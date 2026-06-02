def get_title(response):
    try:
        low_response = response.lower()
    
        start = low_response.find("<title>")
        end = low_response.find("</title>")

        if start != -1 and end != -1:
            start += len("<title>")
            return response[start:end].strip()
        
        return "unknown"
    
    except Exception:
        return "unknown"

def get_content_type(response):
    try:
        for line in response.splitlines():
            if "content-type:" in line.lower():
                return line.split(":", 1)[1].strip()
        return "unknown"
    
    except Exception:
        return "unknown"
    
def http_enum(banner):
    RESULT = {"title"       : get_title(banner),
            "content_Type": get_content_type(banner)}
    return RESULT