from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Response
from api.report_utils import build_pdf_report_bytes

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/pdf")
def export_pdf_report(report_data: Dict[str, Any]):
    try:
        pdf_bytes = build_pdf_report_bytes(report_data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=career_twin_report.pdf",
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(exc)}")


@router.post("/json")
def export_json_report(report_data: Dict[str, Any]) -> Dict[str, Any]:
    return report_data
