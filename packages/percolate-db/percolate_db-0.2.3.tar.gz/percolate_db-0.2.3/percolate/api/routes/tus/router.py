"""
Tus protocol router for the Percolate API.
Implements the tus.io protocol for resumable file uploads.

Tus Protocol Version: 1.0.0
Extensions: creation, expiration, termination, creation-with-upload
"""

import os
import uuid
import base64
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, Response, Header, Depends, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from datetime import timezone
import percolate as p8
from percolate.api.controllers import tus as tus_controller
from percolate.api.controllers.tus import list_pending_s3_resources
from percolate.models.media.tus import (
    TusFileUpload,
    TusFileChunk,
    TusUploadStatus,
    TusUploadMetadata,
    TusUploadPatchResponse,
    TusUploadCreationResponse,
    UserUploadSearchRequest,
    UserUploadSearchResult
)
from percolate.utils import logger
from pydantic import BaseModel
from . import get_project_name
from percolate.api.routes.auth import hybrid_auth, require_user_auth

# Constants for Tus protocol
TUS_VERSION = "1.0.0"
TUS_EXTENSIONS = "creation,creation-with-upload,expiration,termination"
TUS_MAX_SIZE = int(os.environ.get("TUS_MAX_SIZE", str(5 * 1024 * 1024 * 1024)))  # 5GB default
TUS_API_VERSION = os.environ.get("TUS_API_VERSION", "v1")
TUS_API_PATH = os.environ.get("TUS_API_PATH", "/tus")
DEFAULT_EXPIRATION = int(os.environ.get("TUS_DEFAULT_EXPIRATION", "86400"))  # 24 hours in seconds

# Create the router with hybrid authentication required for all endpoints
# This supports both bearer tokens (for testing/API access) and session auth (for users)
router = APIRouter(
    dependencies=[Depends(hybrid_auth)]
)

# Helper functions

def log_model(model: BaseModel, prefix: str = "") -> None:
    """Log the details of a Pydantic model"""
    if not model:
        logger.info(f"{prefix} Model is None")
        return
        
    try:
        # Convert to dict and log
        model_dict = model.model_dump() if hasattr(model, 'model_dump') else model.dict()
        
        # Remove large data fields
        if 'upload_metadata' in model_dict and model_dict['upload_metadata']:
            metadata_size = len(str(model_dict['upload_metadata']))
            model_dict['upload_metadata'] = f"<{metadata_size} bytes of metadata>"
            
        logger.info(f"{prefix} {model.__class__.__name__}: {model_dict}")
    except Exception as e:
        logger.error(f"Error logging model: {str(e)}")

def tus_response_headers(response: Response, upload_id: Optional[str] = None, upload_offset: Optional[int] = None, expiry: Optional[datetime] = None, location: Optional[str] = None):
    """Add standard Tus response headers to a response"""
    response.headers["Tus-Resumable"] = TUS_VERSION
    response.headers["Tus-Version"] = TUS_VERSION
    response.headers["Tus-Extension"] = TUS_EXTENSIONS
    response.headers["Tus-Max-Size"] = str(TUS_MAX_SIZE)
    
    if upload_id and location:
        # Use the absolute URL if provided
        response.headers["Location"] = location
    elif upload_id:
        # Fall back to relative path if no absolute URL provided
        location = f"{TUS_API_PATH}/{upload_id}"
        response.headers["Location"] = location
        
    if upload_offset is not None:
        response.headers["Upload-Offset"] = str(upload_offset)
        
    if expiry:
        response.headers["Upload-Expires"] = expiry.strftime("%a, %d %b %Y %H:%M:%S GMT")

# Tus protocol endpoints

@router.options(
    "/",
    include_in_schema=True,
)
async def tus_options(response: Response):
    """
    Handle OPTIONS request - Tus discovery endpoint
    
    Returns information about the Tus server capabilities
    """
    logger.info("Tus OPTIONS request received")
    
    # Add Tus headers
    tus_response_headers(response)
    
    response.status_code = 204
    return response

@router.post(
    "/",
    status_code=201,
    include_in_schema=True,
)
async def tus_create_upload(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    user_id: Optional[str] = Depends(hybrid_auth),  # Optional - None for bearer auth
    project_name: str = Depends(get_project_name),
    upload_metadata: Optional[str] = Header(None),
    upload_length: Optional[int] = Header(None),
    upload_defer_length: Optional[int] = Header(None),
    content_type: Optional[str] = Header(None),
    content_length: Optional[int] = Header(None),
):
    """
    Handle POST request - Create a new upload
    
    This endpoint creates a new upload and returns its location
    """
    logger.info("Tus upload creation request received")
    
    # Validate Tus version
    if request.headers.get("Tus-Resumable") != TUS_VERSION:
        response.status_code = 412
        response.headers["Tus-Version"] = TUS_VERSION
        return {"error": "Tus version not supported"}
    
    # Validate upload length
    if upload_length is None and upload_defer_length is None:
        response.status_code = 412
        tus_response_headers(response)
        return {"error": "Upload-Length or Upload-Defer-Length required"}
    
    if upload_length is not None and upload_length > TUS_MAX_SIZE:
        response.status_code = 413
        tus_response_headers(response)
        return {"error": "Upload size exceeds maximum allowed"}
    
    # Parse metadata
    metadata = await tus_controller.parse_metadata(upload_metadata or "")
    
    # Get filename from metadata (already base64 decoded by parse_metadata)
    filename = metadata.get("filename", f"upload-{uuid.uuid4()}")
    
    # Extract tags from metadata if available
    tags = None
    if metadata.get("tags"):
        try:
            if isinstance(metadata["tags"], str):
                # Split comma-separated tags
                tags = [tag.strip() for tag in metadata["tags"].split(',') if tag.strip()]
            elif isinstance(metadata["tags"], list):
                tags = metadata["tags"]
            # Limit to 3 tags
            if tags and len(tags) > 3:
                tags = tags[:3]
        except Exception as e:
            logger.warning(f"Error processing tags from metadata: {str(e)}")
    
    # Calculate expiration
    expires_in = timedelta(seconds=DEFAULT_EXPIRATION)
    
    if user_id:
        logger.info(f"Using user ID from session: {user_id}")
    else:
        logger.info("Using bearer token authentication (no user context)")
    
    # Create the upload
    upload_response = await tus_controller.create_upload(
        request=request,
        filename=filename,
        file_size=upload_length or 0,
        metadata=metadata,
        userid=user_id,  # Pass as userid to match the model field
        project_name=project_name,
        content_type=content_type,
        expires_in=expires_in,
        tags=tags
    )
    
    # Log the response model for debugging
    log_model(upload_response, "Upload created:")
    
    # Set Tus response headers
    tus_response_headers(
        response=response, 
        upload_id=str(upload_response.upload_id),
        expiry=upload_response.expires_at,
        location=upload_response.location
    )
    
    # Add Upload-Expires header
    if upload_response.expires_at:
        response.headers["Upload-Expires"] = upload_response.expires_at.strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    # Handle creation-with-upload extension
    if content_length and content_length > 0:
        # Read the body
        body = await request.body()
        
        # Process the chunk
        await tus_controller.process_chunk(
            upload_id=upload_response.upload_id,
            chunk_data=body,
            content_length=content_length,
            offset=0
        )
        
        # Set the offset header
        response.headers["Upload-Offset"] = str(content_length)
    
    response.status_code = 201
    return response

@router.head(
    "/{upload_id}",
    include_in_schema=True,
)
async def tus_upload_info(
    response: Response,
    upload_id: str = Path(...),
):
    """
    Handle HEAD request - Get upload info
    
    This endpoint returns information about an existing upload
    """
    logger.info(f"Tus HEAD request for upload: {upload_id}")
    
    # Get the upload info
    upload = await tus_controller.get_upload_info(upload_id)
    
    # Set Tus response headers
    tus_response_headers(
        response=response,
        upload_id=str(upload.id),
        upload_offset=upload.uploaded_size,
        expiry=upload.expires_at
    )
    
    # Add custom headers
    response.headers["Upload-Length"] = str(upload.total_size)
    response.headers["Upload-Metadata"] = ""  # We could reconstruct this if needed
    
    # Cache control to prevent caching
    response.headers["Cache-Control"] = "no-store"
    
    response.status_code = 200
    return response

@router.patch(
    "/{upload_id}",
    include_in_schema=True,
)
async def tus_upload_chunk(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    upload_id: str = Path(...),
    content_type: Optional[str] = Header(None),
    content_length: Optional[int] = Header(None),
    upload_offset: Optional[int] = Header(None),
):
    """
    Handle PATCH request - Upload a chunk
    
    This endpoint accepts a chunk of data for an existing upload
    """
    logger.info(f"Tus PATCH request for upload: {upload_id}, offset: {upload_offset}")
    
    # Validate Tus version
    if request.headers.get("Tus-Resumable") != TUS_VERSION:
        response.status_code = 412
        response.headers["Tus-Version"] = TUS_VERSION
        return {"error": "Tus version not supported"}
    
    # Validate content type
    if content_type != "application/offset+octet-stream":
        response.status_code = 415
        tus_response_headers(response)
        return {"error": "Content-Type must be application/offset+octet-stream"}
    
    # Validate upload offset
    if upload_offset is None:
        response.status_code = 412
        tus_response_headers(response)
        return {"error": "Upload-Offset header required"}
    
    # Validate content length
    if not content_length or content_length <= 0:
        response.status_code = 412
        tus_response_headers(response)
        return {"error": "Content-Length header required"}
    
    # Get upload info to check current offset
    upload = await tus_controller.get_upload_info(upload_id)
    
    # Verify the offset matches
    if upload.uploaded_size != upload_offset:
        response.status_code = 409
        tus_response_headers(response, upload_id=str(upload.id), upload_offset=upload.uploaded_size)
        return {"error": f"Upload offset does not match: expected {upload.uploaded_size}, got {upload_offset}"}
    
    # Read the chunk data
    chunk_data = await request.body()
    
    # Verify the chunk size matches content length
    if len(chunk_data) != content_length:
        response.status_code = 412
        tus_response_headers(response)
        return {"error": "Content-Length does not match actual data length"}
    
    # Process the chunk
    patch_response = await tus_controller.process_chunk(
        upload_id=upload_id,
        chunk_data=chunk_data,
        content_length=content_length,
        offset=upload_offset,
        background_tasks=background_tasks
    )
    
    # Set Tus response headers
    tus_response_headers(
        response=response,
        upload_id=str(patch_response.upload_id),
        upload_offset=patch_response.offset,
        expiry=patch_response.expires_at
    )
    
    response.status_code = 204
    return response

@router.delete(
    "/{upload_id}",
    include_in_schema=True,
)
async def tus_delete_upload(
    request: Request,
    response: Response,
    upload_id: str = Path(...),
):
    """
    Handle DELETE request - Terminate an upload
    
    This endpoint deletes an upload and all its chunks
    """
    logger.info(f"Tus DELETE request for upload: {upload_id}")
    
    # Validate Tus version
    if request.headers.get("Tus-Resumable") != TUS_VERSION:
        response.status_code = 412
        response.headers["Tus-Version"] = TUS_VERSION
        return {"error": "Tus version not supported"}
    
    # Delete the upload
    await tus_controller.delete_upload(upload_id)
    
    # Set Tus response headers
    tus_response_headers(response)
    
    response.status_code = 204
    return response

# Additional endpoints beyond Tus protocol spec

@router.get(
    "/pending-resources",
    include_in_schema=True,
)
async def get_pending_resources(
    response: Response,
    limit: int = Query(20, gt=0, le=100),
):
    """
    List pending uploads that have been uploaded to S3 but not yet processed into resources.
    
    This endpoint is useful for monitoring and debugging the resource creation process.
    """
    logger.info(f"Listing pending uploads that need resource creation (limit: {limit})")
    
    # Get pending uploads
    pending_uploads = await list_pending_s3_resources(limit=limit)
    
    # Convert to response format
    results = []
    for upload in pending_uploads:
        # Format timestamps
        created_at = upload['created_at'].isoformat() if upload['created_at'] else None
        updated_at = upload['updated_at'].isoformat() if upload['updated_at'] else None
        
        results.append({
            "id": str(upload['id']),
            "filename": upload['filename'],
            "content_type": upload['content_type'],
            "total_size": upload['total_size'],
            "s3_uri": upload['s3_uri'],
            "project_name": upload['project_name'],
            "userid": str(upload['userid']) if upload['userid'] else None,
            "created_at": created_at,
            "updated_at": updated_at
        })
    
    # Return the results
    return {
        "pending_uploads": results,
        "count": len(results),
        "limit": limit
    }

# We no longer create schedules at startup as this is not idempotent
# Instead, admins should use the /create-schedule endpoint to create schedules manually
# and the scheduler will load them from the database

@router.get(
    "/",
    include_in_schema=True,
)
async def list_uploads(
    response: Response,
    user_id: Optional[str] = Depends(hybrid_auth),  # Optional - None for bearer auth
    project_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(100, gt=0, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    List uploads with optional filtering
    
    This endpoint allows listing and filtering uploads by different criteria including tags and text search
    """
    logger.info(f"List uploads request: user={user_id}, project={project_name}, status={status}, tags={tags}, search={search}")
    
    # Convert status string to enum if provided
    status_enum = None
    if status:
        try:
            status_enum = TusUploadStatus(status)
        except ValueError:
            response.status_code = 400
            return {"error": f"Invalid status value: {status}"}
    
    # List uploads
    uploads = await tus_controller.list_uploads(
        user_id=user_id,
        project_name=project_name,
        status=status_enum,
        tags=tags,
        search_text=search,
        limit=limit,
        offset=offset
    )
    
    # Set Tus response headers for consistency
    tus_response_headers(response)
    
    # Return the uploads as JSON
    return {
        "uploads": [upload.model_dump() for upload in uploads],
        "count": len(uploads),
        "limit": limit,
        "offset": offset
    }

@router.post(
    "/process-pending",
    include_in_schema=True,
)
async def process_pending_resources_endpoint(
    response: Response,
    limit: int = Query(20, gt=0, le=100),
):
    """
    Process pending uploads that have been uploaded to S3 but not yet processed into resources.
    
    This endpoint manually triggers the processing of pending uploads.
    """
    logger.info(f"Processing pending uploads (limit: {limit})")
    
    # Process pending uploads
    result = await tus_controller.process_pending_s3_resources(limit=limit)
    
    return result

@router.post(
    "/{upload_id}/finalize",
    include_in_schema=True,
)
async def finalize_upload(
    response: Response,
    background_tasks: BackgroundTasks,
    upload_id: str = Path(...),
):
    """
    Finalize an upload by assembling chunks
    
    This endpoint takes a completed upload and assembles the chunks into a single file
    """
    logger.info(f"Finalize upload request for: {upload_id}")
    
    # Check if upload is already finalized
    try:
        upload = await tus_controller.get_upload_info(upload_id)
        
        # If the upload is already fully processed with S3 URI, return that info
        if (hasattr(upload, 's3_uri') and upload.s3_uri) or upload.upload_metadata.get("s3_uri"):
            logger.info(f"Upload {upload_id} already finalized with S3 URI")
            
            # Return the existing S3 information
            return {
                "upload_id": str(upload.id),
                "filename": upload.filename,
                "size": upload.total_size,
                "content_type": upload.content_type,
                "status": upload.status,
                "s3_uri": upload.s3_uri if hasattr(upload, 's3_uri') and upload.s3_uri else upload.upload_metadata.get("s3_uri", ""),
                "s3_bucket": upload.s3_bucket if hasattr(upload, 's3_bucket') else None,
                "s3_key": upload.s3_key if hasattr(upload, 's3_key') else None,
                "local_path": upload.upload_metadata.get("local_path", "")
            }
            
        # Check if it's marked as locally assembled but pending S3 upload
        if upload.upload_metadata.get("assembly_complete") and upload.upload_metadata.get("needs_s3_upload"):
            logger.info(f"Upload {upload_id} already assembled locally, forcing S3 upload")
            
            # Get the local path
            local_path = upload.upload_metadata.get("local_path")
            if local_path and os.path.exists(local_path):
                # Trigger S3 upload with the background task
                background_tasks.add_task(
                    tus_controller.upload_to_s3_background, 
                    str(upload.id), 
                    local_path
                )
                
                # Return the current state while S3 upload happens in background
                return {
                    "upload_id": str(upload.id),
                    "filename": upload.filename,
                    "size": upload.total_size,
                    "content_type": upload.content_type,
                    "status": upload.status,
                    "local_path": local_path,
                    "s3_status": "processing"
                }
    except Exception as check_error:
        logger.error(f"Error checking upload state: {str(check_error)}")
        # Continue with normal finalization
    
    # Standard finalization process if not already finalized
    logger.info(f"Proceeding with finalization for upload: {upload_id}")
    final_path = await tus_controller.finalize_upload(upload_id, background_tasks)
    
    # Set Tus response headers for consistency
    tus_response_headers(response)
    
    # Get the upload info for response
    upload = await tus_controller.get_upload_info(upload_id)
    
    # Log the upload details
    log_model(upload, "Finalized upload:")
    
    # Log detailed S3 info
    if hasattr(upload, 's3_uri') and upload.s3_uri:
        logger.info(f"File stored in S3 at: Bucket={upload.s3_bucket}, Key={upload.s3_key}, URI={upload.s3_uri}")
    elif upload.upload_metadata.get("s3_uri"):
        logger.info(f"File stored in S3 at: URI={upload.upload_metadata.get('s3_uri')}")
    else:
        logger.info(f"File stored locally at: {final_path}")
    
    # Return success with file information
    return {
        "upload_id": str(upload.id),
        "filename": upload.filename,
        "size": upload.total_size,
        "content_type": upload.content_type,
        "status": upload.status,
        "s3_uri": upload.s3_uri if hasattr(upload, 's3_uri') and upload.s3_uri else upload.upload_metadata.get("s3_uri", ""),
        "s3_bucket": upload.s3_bucket if hasattr(upload, 's3_bucket') else None,
        "s3_key": upload.s3_key if hasattr(upload, 's3_key') else None,
        "local_path": final_path
    }

@router.post(
    "/{upload_id}/extend",
    include_in_schema=True,
)
async def extend_upload_expiration(
    response: Response,
    upload_id: str = Path(...),
    expires_in: int = Query(DEFAULT_EXPIRATION, description="Expiration time in seconds"),
):
    """
    Extend the expiration of an upload
    
    This endpoint extends the expiration time of an upload
    """
    logger.info(f"Extend expiration request for upload: {upload_id}, expires_in: {expires_in}")
    
    # Calculate expiration delta
    expires_delta = timedelta(seconds=expires_in)
    
    # Extend the expiration
    new_expiry = await tus_controller.extend_expiration(upload_id, expires_delta)
    
    # Set Tus response headers
    tus_response_headers(response, expiry=new_expiry)
    
    # Return success with new expiration
    return {
        "upload_id": upload_id,
        "expires_at": new_expiry.isoformat()
    }

@router.get(
    "/user/{user_id}/files",
    include_in_schema=True,
)
async def get_user_files_by_id(
    response: Response,
    user_id: str = Path(..., description="User ID to retrieve files for"),
    limit: int = Query(100, gt=0, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    Get files for a specific user by user ID
    
    This endpoint returns all files uploaded by a specific user ID
    """
    logger.info(f"Request for files of user ID: {user_id}")
    
    # Get files for user
    uploads = await tus_controller.get_user_files(
        user_id=user_id,
        limit=limit,
        offset=offset
    )
    
    # Set Tus response headers for consistency
    tus_response_headers(response)
    
    # Return the files as JSON
    return {
        "user_id": user_id,
        "uploads": [upload.model_dump() for upload in uploads],
        "count": len(uploads),
        "limit": limit,
        "offset": offset
    }

@router.get(
    "/user/recent",
    include_in_schema=True,
)
async def get_recent_user_uploads(
    response: Response,
    user_id: str = Depends(require_user_auth),  # Must have user context
    limit: int = Query(10, gt=0, le=100),
    project_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = Query(None),
):
    """
    Get recent uploads for the authenticated user
    
    This endpoint returns the user's most recent uploads, with optional filtering
    by tags and search text
    """
    logger.info(f"Get recent uploads for user: {user_id}, tags: {tags}, search: {search}")
    
    
    # Convert status string to enum if provided
    status_enum = None
    if status:
        try:
            status_enum = TusUploadStatus(status)
        except ValueError:
            response.status_code = 400
            return {"error": f"Invalid status value: {status}"}
    
    # List uploads for the user
    uploads = await tus_controller.list_uploads(
        user_id=user_id,
        project_name=project_name,
        status=status_enum,
        tags=tags,
        search_text=search,
        limit=limit,
        offset=0
    )
    
    # Set Tus response headers for consistency
    tus_response_headers(response)
    
    # Return the uploads as JSON
    return {
        "user_id": user_id,
        "uploads": [upload.model_dump() for upload in uploads],
        "count": len(uploads)
    }
    
@router.put(
    "/{upload_id}/tags",
    include_in_schema=True,
)
async def update_upload_tags(
    response: Response,
    upload_id: str = Path(...),
    tags: List[str] = Query(..., max_items=3),
    user_id: Optional[str] = Depends(hybrid_auth),  # Optional - None for bearer auth
):
    """
    Update the tags for an upload
    
    This endpoint allows setting up to 3 tags on an upload for categorization and searching
    """
    logger.info(f"Update tags for upload: {upload_id}, tags: {tags}")
    if user_id:
        logger.info(f"Using user ID: {user_id}")
    else:
        logger.info("Using bearer token authentication (admin access)")
    
    try:
        # Get the upload
        upload = await tus_controller.get_upload_info(upload_id)
        
        # Check if user is authorized to modify this upload
        # Bearer token auth allows updates to any upload (admin access)
        # Session auth requires ownership
        if user_id and upload.userid and str(upload.userid) != user_id:
            response.status_code = 403
            return {"error": "Not authorized to modify this upload"}
        
        # Update the tags (limit to 3)
        upload.tags = tags[:3] if len(tags) > 3 else tags
        upload.updated_at = datetime.now(timezone.utc)
        
        # Save the changes
        p8.repository(TusFileUpload).update_records([upload])
        
        # If the upload is in S3, update the metadata there too
        if (upload.upload_metadata.get("storage_type") == "s3" and 
            upload.upload_metadata.get("s3_uri")):
            # Update tags in metadata for S3 search compatibility
            upload.upload_metadata["tags"] = upload.tags
            p8.repository(TusFileUpload).update_records([upload])
        
        # Set Tus response headers for consistency
        tus_response_headers(response)
        
        # Return the updated upload
        return {
            "upload_id": str(upload.id),
            "tags": upload.tags,
            "updated_at": upload.updated_at.isoformat()
        }
 
    except Exception as e:
        logger.error(f"Error updating tags: {str(e)}")
        response.status_code = 500
        return {"error": f"Error updating tags: {str(e)}"}
        
@router.get(
    "/search/semantic",
    include_in_schema=True,
)
async def semantic_search(
    response: Response,
    query: str = Query(..., min_length=3),
    user_id: Optional[str] = Depends(hybrid_auth),  # Optional - None for bearer auth
    project_name: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    limit: int = Query(10, gt=0, le=100),
):
    """
    Semantic search for files using natural language
    
    This endpoint allows searching for files using semantic similarity
    to the provided query. This is a placeholder for future semantic
    search implementation.
    """
    logger.info(f"Semantic search request: query={query}, user={user_id}, project={project_name}")
    
    # Set Tus response headers for consistency
    tus_response_headers(response)
    
    # For now, just use basic text search as a placeholder
    # In the future, this will use semantic embeddings to find similar content
    uploads = await tus_controller.list_uploads(
        user_id=user_id,
        project_name=project_name,
        tags=tags,
        search_text=query,
        limit=limit,
        offset=0
    )
    
    # Return with a note that this is a placeholder implementation
    return {
        "query": query,
        "results": [upload.model_dump() for upload in uploads],
        "count": len(uploads),
        "implementation": "placeholder_text_search",
        "note": "This is a placeholder for semantic search. Currently using basic text matching."
    }


@router.post(
    "/create-schedule",
    include_in_schema=True,
)
async def create_flush_schedule_endpoint(
    response: Response,
    interval_hours: int = Query(1, gt=0, le=24),
    user_id: Optional[str] = Depends(hybrid_auth),  # Optional - None for bearer auth
):
    """
    Create a scheduled job to periodically process pending uploads.
    
    This endpoint creates a scheduled job that will automatically run
    process_pending_s3_resources at the specified interval.
    """
    logger.info(f"Creating schedule to process pending uploads every {interval_hours} hour(s)")
    
    # Create the schedule
    result = await tus_controller.create_flush_pending_resources_schedule(
        interval_hours=interval_hours,
        user_id=user_id
    )
    
    return result

@router.post(
    "/user/uploads/search",
    response_model=List[UserUploadSearchResult],
    include_in_schema=True,
)
async def search_user_uploads(
    request: UserUploadSearchRequest,
    response: Response,
    user_id: str = Depends(require_user_auth),  # Must have user context
):
    """
    Search user uploads with semantic search and tag filtering
    
    This endpoint allows users to search their uploads using:
    - Semantic search: Find files based on content similarity
    - Tag filtering: Filter by assigned tags
    - Combined search: Use both semantic search and tags together
    
    Returns the top N files based on the search criteria
    """
    logger.info(f"User upload search request: user={user_id}, query={request.query_text}, tags={request.tags}, limit={request.limit}")
    
    # Get PostgreSQL service
    from percolate.services import PostgresService
    pg = PostgresService()
    
    # Call the SQL function using PostgresService
    query = """
        SELECT * FROM p8.file_upload_search(
            p_user_id := %s,
            p_query_text := %s,
            p_tags := %s,
            p_limit := %s
        )
    """
    
    params = [
        user_id,
        request.query_text,
        request.tags if request.tags else None,  # Pass None if no tags
        request.limit
    ]
    
    try:
        # Execute the query
        results = pg.execute(query, params)
        
        # Convert results to UserUploadSearchResult objects
        search_results = []
        for row in results:
            # Handle both dict and tuple results from PostgreSQL
            if isinstance(row, dict):
                data = row
            else:
                # If tuple, convert to dict using column names
                columns = ['upload_id', 'filename', 'content_type', 'total_size', 'uploaded_size',
                          'status', 'created_at', 'updated_at', 's3_uri', 'tags', 'resource_id',
                          'resource_uri', 'resource_name', 'chunk_count', 'resource_size', 
                          'indexed_at', 'semantic_score']
                data = dict(zip(columns, row))
            
            result = UserUploadSearchResult(
                upload_id=data['upload_id'],
                filename=data['filename'],
                content_type=data['content_type'],
                total_size=data['total_size'],
                uploaded_size=data['uploaded_size'],
                status=data['status'],
                created_at=data['created_at'],
                updated_at=data['updated_at'],
                s3_uri=data['s3_uri'],
                tags=data['tags'] if data['tags'] else [],
                resource_id=data['resource_id'],
                # Resource fields (may be None)
                resource_uri=data.get('resource_uri'),
                resource_name=data.get('resource_name'),
                chunk_count=data.get('chunk_count'),
                resource_size=data.get('resource_size'),
                indexed_at=data.get('indexed_at'),
                semantic_score=data.get('semantic_score')
            )
            search_results.append(result)
        
        # Log search summary
        if request.query_text and any(r.semantic_score for r in search_results):
            logger.info(f"Semantic search completed: {len(search_results)} results with scores")
        else:
            logger.info(f"Standard search completed: {len(search_results)} results")
        
        # Set Tus response headers for consistency
        tus_response_headers(response)
        
        return search_results
        
    except Exception as e:
        logger.error(f"Error searching uploads: {str(e)}")
        response.status_code = 500
        # Return empty array instead of error object to match response_model
        return []


@router.get(
    "/user/uploads",
    response_model=List[UserUploadSearchResult],
    include_in_schema=True,
)
async def get_user_uploads(
    response: Response,
    user_id: str = Depends(require_user_auth),  # Must have user context
    query: Optional[str] = Query(None, description="Semantic search query"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    limit: int = Query(20, gt=0, le=100, description="Maximum results to return"),
):
    """
    Get user uploads with optional search and filtering (GET version)
    
    This is a GET endpoint version of the search functionality for convenience.
    Supports the same search capabilities as the POST endpoint:
    - Semantic search: Find files based on content similarity
    - Tag filtering: Filter by assigned tags
    - Combined search: Use both semantic search and tags together
    """
  
    # Create request object and delegate to POST endpoint
    search_request = UserUploadSearchRequest(
        query_text=query,
        tags=tags,
        limit=limit
    )
    
    logger.info(f"Requesting user uploads {user_id=} {search_request=}")
    
    
    return await search_user_uploads(search_request, response, user_id)