import asyncio
from pydantic import Field
from dotenv import load_dotenv
from typing import List, Dict, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from mcp.server.fastmcp import FastMCP
from grabba import (
    Grabba, Job, JobResult, 
    GetJobResponse, GetJobsResponse, JobExecutionStatus,
    GetJobResultResponse, JobExecutionResponse
)


# Settings for the MCP service
class ServerConfig(BaseSettings):
    API_KEY: str = Field(..., description="The API key for accessing the Grabba python SDK.", env="GRABBA_API_KEY")
    MCP_SERVER_TRANSPORT: str = Field("stdio", description="The transport protocol for the MCP server: 'http' or 'stdio'.", env="GRABBA_MCP_SERVER_TRANSPORT")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="GRABBA_",
        extra="ignore"
    )


class GrabbaService:
    def __init__(self, api_key: str):
        self.grabba = Grabba(api_key)

    async def extract_data(self, extraction_data: Job) -> tuple[str, Optional[Dict]]:
        """Schedule a new data extraction job"""
        try:
            result: JobExecutionResponse = self.grabba.extract(job=extraction_data)
            if result.status == JobExecutionStatus.SUCCESS:
                job_result: JobResult = result.job_result
                return result.message, job_result
            return result.message, result.job_result
        except Exception as err:
            return f"Error scheduling job: {str(err)}", None

    async def schedule_job(self, job_id: str) -> tuple[str, Optional[Dict]]:
        """Schedule an existing job to run immediately"""
        try:
            result: JobExecutionResponse = self.grabba.schedule_job(job_id=job_id)
            return result.message, result.job_result
        except Exception as err:
            return f"Error scheduling job: {str(err)}", None

    async def fetch_jobs_data(self) -> tuple[str, Optional[List[Job]]]:
        """Fetch all jobs for the current user"""
        try:
            result: GetJobsResponse = self.grabba.get_jobs()
            return result.message, result.jobs
        except Exception as err:
            return f"Error fetching jobs: {str(err)}", None

    async def fetch_job_data(self, job_id: str) -> tuple[str, Optional[Job]]:
        """Fetch details of a specific job"""
        try:
            result: GetJobResponse = self.grabba.get_job(job_id)
            return result.message, result.job
        except Exception as err:
            return f"Error fetching job: {str(err)}", None

    async def delete_job_data(self, job_id: str) -> tuple[str, None]:
        """Delete a specific job"""
        try:
            self.grabba.delete_job(job_id)
            return f"Successfully deleted job {job_id}", None
        except Exception as err:
            return f"Error deleting job: {str(err)}", None

    async def fetch_job_result_data(self, job_result_id: str) -> tuple[str, Optional[Dict]]:
        """Fetch results of a completed job"""
        try:
            result: GetJobResultResponse = self.grabba.get_job_result(job_result_id)
            return result.message, result.job_result
        except Exception as err:
            return f"Error fetching job results: {str(err)}", None

    async def delete_job_result_data(self, job_result_id: str) -> tuple[str, None]:
        """Delete results of a completed job"""
        try:
            self.grabba.delete_job_result(job_result_id)
            return f"Successfully deleted job result {job_result_id}", None
        except Exception as err:
            return f"Error deleting job results: {str(err)}", None


class GrabbaMcpServer(FastMCP):
    """
    An MCP server exposing Grabba functionalities as tools.
    """
    grabba_service: GrabbaService

    def __init__(self, grabba_service: GrabbaService):
        super().__init__(name="grabba-agent", version="0.0.1")
        self.dependencies = ["grabba"]
        self.grabba_service = grabba_service
        self._register_tools()

    def _register_tools(self):
        """Register GrabbaService methods as MCP tools."""

        self.add_tool(
            self.grabba_service.extract_data,
            name="extract_data",
            description="Schedules a new data extraction job with Grabba. Requires a 'Job' object detailing the extraction tasks.",
        )

        self.add_tool(
            self.grabba_service.schedule_job,
            name="schedule_existing_job",
            description="Schedules an existing Grabba job to run immediately. Requires the 'job_id' of the existing job.",
        )

        self.add_tool(
            self.grabba_service.fetch_jobs_data,
            name="fetch_all_jobs",
            description="Fetches all Grabba jobs for the current user. Takes no parameters.",
        )

        self.add_tool(
            self.grabba_service.fetch_job_data,
            name="fetch_specific_job",
            description="Fetches details of a specific Grabba job by its ID. Requires the 'job_id' of the job.",
        )

        self.add_tool(
            self.grabba_service.delete_job_data,
            name="delete_job",
            description="Deletes a specific Grabba job. Requires the 'job_id' of the job to delete.",
        )

        self.add_tool(
            self.grabba_service.fetch_job_result_data,
            name="fetch_job_result",
            description="Fetches results of a completed Grabba job by its result ID. Requires the 'job_result_id' of the result.",
        )

        self.add_tool(
            self.grabba_service.delete_job_result_data,
            name="delete_job_result",
            description="Deletes results of a completed Grabba job. Requires the 'job_result_id' of the result to delete.",
        )


# Load environment variables from .env file
load_dotenv()

# Instantiate ServerConfig
server_config = ServerConfig()

# Initialize GrabbaService (will use API_KEY from .env)
grabba_service = GrabbaService(server_config.API_KEY)

# Initialize the MCP server
server = GrabbaMcpServer(grabba_service)

def main():
    if server_config.MCP_SERVER_TRANSPORT == "streamable-http":
        server.settings.streamable_http_path = "/"
        # Start the MCP server using FastMCP's built-in run method
        # This will handle HTTP communication protocol (e.g., streamable-http)
        print("Starting Grabba MCP server (streamable-http transport)...")
        asyncio.run(server.run_streamable_http_async())
    elif server_config.MCP_SERVER_TRANSPORT == "sse":
        server.settings.sse_path = "/"
        # Start the MCP server using FastMCP's built-in run method
        # This will handle SSE communication protocol
        print("Starting Grabba MCP server (sse transport)...")
        asyncio.run(server.run_sse_async())
    else:
        # Start the MCP server using StdioTransport
        print("Starting Grabba MCP server (stdio transport)...")
        asyncio.run(server.run())


if __name__ == "__main__":
    main()
