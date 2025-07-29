

import http
import json
from typing import List

import aiohttp
from lanraragi.clients.api_clients.base import ApiClient
from lanraragi.clients.utils import build_err_response
from lanraragi.models.generics import LRRClientResponse
from lanraragi.clients.res_processors.archive import (
    process_get_all_archives_response,
    process_get_archive_categories_response,
    process_get_archive_metadata_response,
    process_get_archive_thumbnail_response
)
from lanraragi.models.archive import (
    GetArchiveMetadataResponse,
    GetArchiveTankoubonsRequest,
    ClearNewArchiveFlagRequest,
    ClearNewArchiveFlagResponse,
    DeleteArchiveRequest,
    DeleteArchiveResponse,
    DownloadArchiveRequest,
    DownloadArchiveResponse,
    ExtractArchiveRequest,
    ExtractArchiveResponse,
    GetAllArchivesResponse,
    GetArchiveCategoriesRequest,
    GetArchiveCategoriesResponse,
    GetArchiveMetadataRequest,
    GetArchiveTankoubonsResponse,
    GetArchiveThumbnailRequest,
    GetArchiveThumbnailResponse,
    GetUntaggedArchivesResponse,
    QueueArchiveThumbnailExtractionRequest,
    QueueArchiveThumbnailExtractionResponse,
    UpdateArchiveMetadataRequest,
    UpdateArchiveThumbnailRequest,
    UpdateArchiveThumbnailResponse,
    UpdateReadingProgressionRequest,
    UpdateReadingProgressionResponse,
    UploadArchiveRequest,
    UploadArchiveResponse
)
from lanraragi.models.base import LanraragiResponse

class ArchiveApiClient(ApiClient):

    async def get_all_archives(self) -> LRRClientResponse[GetAllArchivesResponse]:
        """
        GET /api/archives
        """
        url = self.api_context.build_url("/api/archives")
        status, content = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers)
        if status == 200:
            return (process_get_all_archives_response(content), None)
        return (None, build_err_response(content, status))
    
    async def get_untagged_archives(self) -> LRRClientResponse[GetUntaggedArchivesResponse]:
        """
        GET /api/archives/untagged
        """
        url = self.api_context.build_url("/api/archives/untagged")
        status, content = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers)
        if status == 200:
            return (GetUntaggedArchivesResponse(data=json.loads(content)), None) # the content data should just be a list of string.
        return (None, build_err_response(content, status))
    
    async def get_archive_metadata(self, request: GetArchiveMetadataRequest) -> LRRClientResponse[GetArchiveMetadataResponse]:
        """
        GET /api/archives/:id/metadata
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/metadata")
        status, content = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers)
        if status == 200:
            return (process_get_archive_metadata_response(content), None)
        return (None, build_err_response(content, status))

    async def get_archive_categories(self, request: GetArchiveCategoriesRequest) -> LRRClientResponse[GetArchiveCategoriesResponse]:
        """
        GET /api/archives/:id/categories
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/categories")
        status, content = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers)
        if status == 200:
            return (process_get_archive_categories_response(content), None)
        return (None, build_err_response(content, status))
    
    async def get_archive_tankoubons(self, request: GetArchiveTankoubonsRequest) -> LRRClientResponse[GetArchiveTankoubonsResponse]:
        """
        GET /api/archives/:id/tankoubons
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/tankoubons")
        status, content = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers)
        if status == 200:
            response_j = json.loads(content)
            tankoubons: List[str] = response_j.get("tankoubons")
            return (GetArchiveTankoubonsResponse(tankoubons=tankoubons), None)
        return (None, build_err_response(content, status))
    
    async def get_archive_thumbnail(self, request: GetArchiveThumbnailRequest) -> LRRClientResponse[GetArchiveThumbnailResponse]:
        """
        GET /api/archives/:id/thumbnail
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/thumbnail")
        params = {}
        if request.page:
            params["page"] = request.page
        if request.nofallback:
            params["nofallback"] = request.nofallback
        status, data = await self.api_context.download_thumbnail(url, self.api_context.headers, params=params)
        if status in [200, 202]:
            return (process_get_archive_thumbnail_response(data, status), None)
        return (None, build_err_response(data, status))
    
    async def queue_archive_thumbnail_extraction(self, request: QueueArchiveThumbnailExtractionRequest) -> LRRClientResponse[QueueArchiveThumbnailExtractionResponse]:
        """
        POST /api/archives/:id/files/thumbnails
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/files/thumbnails")
        form_data = aiohttp.FormData(quote_fields=False)
        if request.force:
            form_data.add_field('force', request.force)
        status, data = await self.api_context.handle_request(http.HTTPMethod.POST, url, self.api_context.headers, data=form_data)
        if status in [200, 202]:
            response_j = json.loads(data)
            job = response_j.get("job")
            message = response_j.get("message")
            return (QueueArchiveThumbnailExtractionResponse(job=job, message=message), None)
        return (None, build_err_response(data, status))

    async def download_archive(self, request: DownloadArchiveRequest) -> LRRClientResponse[DownloadArchiveResponse]:
        """
        GET  /api/archives/:id/download
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/download")
        status, data = await self.api_context.download_file(url, self.api_context.headers)
        if status == 200:
            return (DownloadArchiveResponse(data=data), None)
        return (None, build_err_response(data, status))
    
    async def extract_archive(self, request: ExtractArchiveRequest) -> LRRClientResponse[ExtractArchiveResponse]:
        """
        GET /api/archives/:id/files
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/files")
        params = {}
        if request.force:
            params["force"] = request.force
        status, data = await self.api_context.handle_request(http.HTTPMethod.GET, url, self.api_context.headers, params=params)
        if status == 200:
            response_j = json.loads(data)
            job = response_j.get("job")
            pages = response_j.get("pages")
            return (ExtractArchiveResponse(job=job, pages=pages), None)
        return (None, build_err_response(data, status))
    
    async def clear_new_archive_flag(self, request: ClearNewArchiveFlagRequest) -> LRRClientResponse[ClearNewArchiveFlagResponse]:
        """
        DELETE /api/archives/:id/isnew
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/isnew")
        status, content = await self.api_context.handle_request(http.HTTPMethod.DELETE, url, self.api_context.headers)
        if status == 200:
            return (ClearNewArchiveFlagResponse(arcid=request.arcid), None)
        return (None, build_err_response(content, status))
    
    async def update_reading_progression(self, request: UpdateReadingProgressionRequest) -> LRRClientResponse[UpdateReadingProgressionResponse]:
        """
        PUT /api/archives/:id/progress/:page
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/progress/{request.page}")
        status, content = await self.api_context.handle_request(http.HTTPMethod.PUT, url, self.api_context.headers)
        if status == 200:
            response_j = json.loads(content)
            arcid = response_j.get("id")
            page = response_j.get("page")
            lastreadtime = response_j.get("lastreadtime")
            return (UpdateReadingProgressionResponse(arcid=arcid, page=page, lastreadtime=lastreadtime), None)
        return (None, build_err_response(content, status))
    
    async def upload_archive(self, request: UploadArchiveRequest) -> LRRClientResponse[UploadArchiveResponse]:
        """
        PUT /api/archives/upload
        """
        url = self.api_context.build_url("/api/archives/upload")
        form_data = aiohttp.FormData(quote_fields=False)
        form_data.add_field('file', request.file, filename=request.filename, content_type='application/octet-stream')
        if request.title:
            form_data.add_field('title', request.title)
        if request.tags:
            form_data.add_field('tags', request.tags)
        if request.summary:
            form_data.add_field('summary', request.summary)
        if request.category_id:
            form_data.add_field('category_id', request.category_id)
        if request.file_checksum:
            form_data.add_field('file_checksum', request.file_checksum)
        status, content = await self.api_context.handle_request(http.HTTPMethod.PUT, url, self.api_context.headers, data=form_data)
        if status == 200:
            response_j = json.loads(content)
            arcid = response_j.get("id")
            filename = response_j.get("filename")
            return (UploadArchiveResponse(arcid=arcid, filename=filename), None)
        return (None, build_err_response(content, status))
    
    async def update_thumbnail(self, request: UpdateArchiveThumbnailRequest) -> LRRClientResponse[UpdateArchiveThumbnailResponse]:
        """
        PUT /api/archives/:id/thumbnail
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/thumbnail")
        form_data = aiohttp.FormData(quote_fields=False)
        form_data.add_field('page', request.page)
        status, content = await self.api_context.handle_request(http.HTTPMethod.PUT, url, self.api_context.headers, data=form_data)
        if status == 200:
            response_j = json.loads(content)
            new_thumbnail = response_j.get("new_thumbnail")
            return (UpdateArchiveThumbnailResponse(new_thumbnail=new_thumbnail), None)
        return (None, build_err_response(content, status))
    
    async def update_archive_metadata(self, request: UpdateArchiveMetadataRequest) -> LRRClientResponse[LanraragiResponse]:
        """
        PUT /api/archives/:id/metadata
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}/metadata")
        form_data = aiohttp.FormData(quote_fields=False)
        if request.title:
            form_data.add_field('title', request.title)
        if request.tags:
            form_data.add_field('tags', request.tags)
        if request.summary:
            form_data.add_field('summary', request.summary)
        status, content = await self.api_context.handle_request(http.HTTPMethod.PUT, url, self.api_context.headers, data=form_data)
        if status == 200:
            return (LanraragiResponse(), None)
        return (None, build_err_response(content, status))
    
    async def delete_archive(self, request: DeleteArchiveRequest) -> LRRClientResponse[DeleteArchiveResponse]:
        """
        DELETE /api/archives/:id
        """
        url = self.api_context.build_url(f"/api/archives/{request.arcid}")
        status, content = await self.api_context.handle_request(http.HTTPMethod.DELETE, url, self.api_context.headers)
        if status == 200:
            response_j = json.loads(content)
            filename = response_j.get("filename")
            return (DeleteArchiveResponse(arcid=request.arcid, filename=filename), None)
        return (None, build_err_response(content, status))
