"""PDF export for case reports."""
import os
import json
from datetime import datetime
from typing import Dict, Any

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "storage", "exports", "pdf")
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_case_pdf(ticket_id: str, case: Dict[str, Any]) -> str:
    """Export a case to PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import inch
    except ImportError:
        # Fallback to HTML export if reportlab not available
        return export_case_html(ticket_id, case)
    
    filename = f"{ticket_id}.pdf"
    filepath = os.path.join(EXPORT_DIR, filename)
    
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "REFORGE OS - Case Report")
    
    # Ticket ID
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, f"Ticket ID: {ticket_id}")
    
    # Timestamp
    timestamp = case.get("timestamp") or case.get("saved_at") or datetime.utcnow().isoformat()
    c.drawString(1*inch, height - 1.75*inch, f"Date: {timestamp}")
    
    # Case Type
    case_type = case.get("type", "unknown")
    c.drawString(1*inch, height - 2*inch, f"Type: {case_type.upper()}")
    
    # Content
    y_pos = height - 2.5*inch
    c.setFont("Helvetica", 10)
    
    if case_type == "diagnostic":
        device = case.get("device", {})
        results = case.get("results", {})
        
        text = f"""
Device Information:
- Model: {device.get('model', 'Unknown')}
- Platform: {device.get('platform', 'Unknown')}

Results:
{json.dumps(results, indent=2)}
"""
    elif case_type == "devmode":
        profile = case.get("profile", {})
        module = case.get("module", "unknown")
        output = case.get("output", "")
        
        text = f"""
Profile: {profile.get('name', 'Unknown')}
Module: {module}

Output:
{output[:2000]}  # Limit to 2000 chars
"""
    else:
        text = json.dumps(case, indent=2)
    
    # Draw text (simplified)
    lines = text.splitlines()
    for line in lines[:50]:  # Limit to 50 lines
        if y_pos < 1*inch:
            c.showPage()
            y_pos = height - 1*inch
        c.drawString(1*inch, y_pos, line[:100])  # Limit line length
        y_pos -= 0.25*inch
    
    c.save()
    return filepath


def export_case_html(ticket_id: str, case: Dict[str, Any]) -> str:
    """Export a case to HTML (fallback if PDF not available)."""
    export_dir = os.path.join(os.path.dirname(__file__), "..", "storage", "exports", "html")
    os.makedirs(export_dir, exist_ok=True)
    
    filename = f"{ticket_id}.html"
    filepath = os.path.join(export_dir, filename)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Case Report - {ticket_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 2em; }}
        h1 {{ color: #333; }}
        pre {{ background: #f5f5f5; padding: 1em; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>REFORGE OS - Case Report</h1>
    <p><strong>Ticket ID:</strong> {ticket_id}</p>
    <p><strong>Date:</strong> {case.get('timestamp', case.get('saved_at', 'Unknown'))}</p>
    <p><strong>Type:</strong> {case.get('type', 'unknown')}</p>
    <hr>
    <pre>{json.dumps(case, indent=2)}</pre>
</body>
</html>
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    
    return filepath
