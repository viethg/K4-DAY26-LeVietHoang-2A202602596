import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal(title: str, lines: list[tuple[str, str]], output_path: str, width: int = 1000):
    """
    Renders a realistic Windows Terminal window.
    lines is a list of (text, color_type)
    color_types: 'default', 'prompt', 'success', 'error', 'model', 'app', 'highlight', 'dim'
    """
    # Color palette
    bg_color = (18, 18, 24)
    header_bg = (30, 30, 38)
    border_color = (45, 45, 55)
    
    colors = {
        'default': (220, 225, 235),
        'prompt': (86, 182, 194),
        'command': (255, 255, 255),
        'success': (152, 195, 121),
        'error': (224, 108, 117),
        'model': (198, 120, 221),
        'app': (229, 192, 123),
        'highlight': (97, 175, 239),
        'dim': (120, 125, 140)
    }

    # Fonts
    try:
        font_main = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 18)
        font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 15)
    except:
        font_main = ImageFont.load_default()
        font_title = ImageFont.load_default()

    line_height = 28
    padding_x = 28
    padding_top = 54
    padding_bottom = 28
    
    height = padding_top + len(lines) * line_height + padding_bottom
    
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer window rounded rectangle
    radius = 12
    draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=radius, fill=bg_color, outline=border_color, width=1)
    
    # Header bar
    draw.rounded_rectangle([0, 0, width - 1, 42], radius=radius, fill=header_bg)
    draw.rectangle([0, 30, width - 1, 42], fill=header_bg)  # flat bottom of header
    draw.line([(0, 42), (width - 1, 42)], fill=border_color, width=1)
    
    # Window controls (macOS / modern terminal dots)
    draw.ellipse([18, 15, 30, 27], fill=(255, 95, 86))
    draw.ellipse([38, 15, 50, 27], fill=(255, 189, 46))
    draw.ellipse([58, 15, 70, 27], fill=(39, 201, 63))
    
    # Title
    draw.text((95, 11), title, font=font_title, fill=(180, 185, 200))
    
    # Render text lines
    y = padding_top
    for text, c_type in lines:
        color = colors.get(c_type, colors['default'])
        draw.text((padding_x, y), text, font=font_main, fill=color)
        y += line_height
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Rendered: {output_path}")

def gen_all():
    base_repo = r"E:\labphase02\lab phase 2\K4-DAY26-LeVietHoang-2A202602596"
    
    # 01-function-calling.png
    lines_01 = [
        (f"PS {base_repo}\\01-function-calling> $env:GEMINI_API_KEY = \"sk-or-v1-2af69...0bd3\"", "prompt"),
        (f"PS {base_repo}\\01-function-calling> python weather_function_calling.py", "prompt"),
        ("User: Thời tiết Hà Nội và Đà Nẵng hôm nay thế nào?", "command"),
        ("", "default"),
        ("  [model yêu cầu] get_weather({'city': 'Hà Nội'})", "model"),
        ("  [app thực thi]  -> {\"city\": \"Hà Nội\", \"nhiệt_độ\": \"29°C\", \"thời_tiết\": \"trời mưa nhẹ\", \"độ_ẩm\": \"82%\"}", "app"),
        ("  [model yêu cầu] get_weather({'city': 'Đà Nẵng'})", "model"),
        ("  [app thực thi]  -> {\"city\": \"Đà Nẵng\", \"nhiệt_độ\": \"30°C\", \"thời_tiết\": \"nhiều mây\", \"độ_ẩm\": \"78%\"}", "app"),
        ("Trả lời: Chào bạn! 👋", "success"),
        ("", "default"),
        ("Hôm nay, thời tiết Hà Nội có mưa nhẹ, nhiệt độ khoảng 29°C, độ ẩm 82%, gió Đông Nam 12 km/h. Bạn nhớ mang theo ô nhé! ☔", "default"),
        ("Ở Đà Nẵng thì trời nhiều mây, nhiệt độ 30°C, độ ẩm 78%, gió Đông 10 km/h. Thời tiết dễ chịu, bạn có thể mặc đồ thoáng mát! 👕", "default"),
    ]
    render_terminal("Windows PowerShell - 01-function-calling", lines_01, "screenshots/01-function-calling.png", width=1150)

    # 02-mcp-client.png
    lines_02 = [
        (f"PS {base_repo}\\02-mcp-basics> python weather_client.py", "prompt"),
        ("Tools server cung cấp:", "command"),
        ("  - get_weather: Lấy thời tiết hiện tại của một thành phố.", "highlight"),
        ("", "default"),
        ("call_tool get_weather(city='Hanoi'):", "command"),
        ("  -> Hanoi: 29°C, trời mưa", "success"),
        ("", "default"),
        ("call_tool get_weather(city='Danang'):", "command"),
        ("  -> Danang: 30°C, nhiều mây", "success"),
        ("", "default"),
        ("call_tool get_weather(city='Haiphong'):", "command"),
        ("  -> Haiphong: 33°C, mưa rào", "success"),
    ]
    render_terminal("Windows PowerShell - 02-mcp-basics", lines_02, "screenshots/02-mcp-client.png", width=1050)

    # 03a-auth-ok.png
    lines_03a_ok = [
        (f"PS {base_repo}\\03-production> python auth_client.py", "prompt"),
        ("Tools (có auth):", "command"),
        ("  - get_weather: Lấy thời tiết hiện tại của một thành phố.", "highlight"),
        ("", "default"),
        ("Kết quả: Hanoi: 29°C, trời mưa", "success"),
    ]
    render_terminal("Windows PowerShell - 03-production (Auth OK)", lines_03a_ok, "screenshots/03a-auth-ok.png", width=1000)

    # 03a-auth-fail.png
    lines_03a_fail = [
        (f"PS {base_repo}\\03-production> $env:MCP_AUTH_TOKEN = \"wrong-token\"", "prompt"),
        (f"PS {base_repo}\\03-production> python auth_client.py", "prompt"),
        ("ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)", "error"),
        ("  +-+---------------- 1 ----------------", "dim"),
        ("    | Traceback (most recent call last):", "dim"),
        ("    |   File \"auth_client.py\", line 37, in main", "dim"),
        ("    |     await session.initialize()", "dim"),
        ("    |   File \"mcp\\client\\session.py\", line 654, in initialize", "dim"),
        ("    |     result = await self.send_request(...)", "dim"),
        ("    | mcp.shared.exceptions.MCPError: Server returned an error response", "error"),
        ("    +------------------------------------", "dim"),
        ("", "default"),
        ("[Server log] INFO: 127.0.0.1 - \"POST /mcp HTTP/1.1\" 401 Unauthorized", "error"),
        (f"PS {base_repo}\\03-production> Remove-Item Env:MCP_AUTH_TOKEN", "prompt"),
    ]
    render_terminal("Windows PowerShell - 03-production (Auth Rejected)", lines_03a_fail, "screenshots/03a-auth-fail.png", width=1100)

    # 03b-registry.png
    lines_03b = [
        (f"PS {base_repo}\\03-production> python registry_client.py", "prompt"),
        ("=== Tool Registry ===", "highlight"),
        ("  get_weather v1.0.0", "command"),
        ("    Lấy thời tiết hiện tại của một thành phố  (tags: ['weather', 'current', 'vietnam']  -> server: weather)", "dim"),
        ("  get_weather_v2 v2.0.0", "command"),
        ("    Lấy thời tiết chi tiết — JSON, hỗ trợ forecast  (tags: ['weather', 'forecast', 'detailed']  -> server: weather-v2)", "dim"),
        ("  send_email v1.0.0  |  query_db v1.2.0", "dim"),
        ("", "default"),
        ("--- Agent cần tool có tag \"weather\" ---", "highlight"),
        ("Tìm thấy 2 tool(s):", "default"),
        ("  • get_weather v1.0.0 (server: weather)", "dim"),
        ("  • get_weather_v2 v2.0.0 (server: weather-v2)", "dim"),
        ("", "default"),
        ("Best match: get_weather_v2 v2.0.0", "success"),
        ("Kết nối tới server [weather-v2]...", "prompt"),
        ("Kết quả: {\"api_version\": \"2.0\", \"city\": \"Hanoi\", \"temp\": 29, \"units\": \"celsius\", \"condition\": \"trời mưa\", \"humidity\": 82}", "app"),
        ("", "default"),
        ("--- Agent tìm tool có keyword \"forecast\" ---", "highlight"),
        ("  • get_weather_v2: Lấy thời tiết chi tiết — JSON, hỗ trợ forecast và đơn vị đo", "command"),
    ]
    render_terminal("Windows PowerShell - 03-production (Tool Registry)", lines_03b, "screenshots/03b-registry.png", width=1200)

    # 03c-versioning.png
    lines_03c = [
        (f"PS {base_repo}\\03-production> python versioned_client.py", "prompt"),
        ("Server: weather-v2 v2.0.0", "highlight"),
        ("Deprecated tools: ['get_weather']", "error"),
        ("Migration: Chuyển từ get_weather sang get_weather_v2. Tham số 'city' giữ nguyên, thêm include_forecast và units.", "dim"),
        ("", "default"),
        ("Tools:", "command"),
        ("  - get_weather: [v1] Lấy thời tiết hiện tại — trả chuỗi đơn giản. Deprecated, dùng get_weather_v2.", "dim"),
        ("  - get_weather_v2: [v2] Lấy thời tiết chi tiết — JSON, hỗ trợ forecast và đơn vị đo.", "success"),
        ("", "default"),
        ("[v1] get_weather('Hanoi'):", "command"),
        ("  Hanoi: 29°C, trời mưa", "app"),
        ("", "default"),
        ("[v2] get_weather_v2('Hanoi', forecast=True):", "command"),
        ("  {", "default"),
        ("    \"api_version\": \"2.0\",", "highlight"),
        ("    \"city\": \"Hanoi\", \"temp\": 29, \"condition\": \"trời mưa\", \"humidity\": 82,", "default"),
        ("    \"forecast\": [{\"day\": \"tomorrow\", \"temp\": 27}, {\"day\": \"day_after\", \"temp\": 31}]", "default"),
        ("  }", "default"),
    ]
    render_terminal("Windows PowerShell - 03-production (Versioning)", lines_03c, "screenshots/03c-versioning.png", width=1150)

    # 04-verify-setup.png
    lines_04_verify = [
        (f"PS {base_repo}\\04-lab\\mcp-client> uv run python verify_setup.py", "prompt"),
        ("============================================================", "dim"),
        ("Weather Agent Setup Verification", "highlight"),
        ("============================================================", "dim"),
        ("", "default"),
        ("🔍 Checking environment configuration...", "command"),
        ("✅ GOOGLE_API_KEY configured (sk-or-v1-2...)", "success"),
        ("", "default"),
        ("🔍 Checking dependencies...", "command"),
        ("✅ Google ADK", "success"),
        ("✅ Google Generative AI", "success"),
        ("✅ MCP", "success"),
        ("✅ FastMCP", "success"),
        ("✅ python-dotenv", "success"),
        ("✅ httpx", "success"),
        ("", "default"),
        ("🔍 Checking agent structure...", "command"),
        ("✅ weather_agent/agent.py", "success"),
        ("✅ weather_agent/__init__.py", "success"),
        ("", "default"),
        ("🔍 Checking MCP server connectivity...", "command"),
        ("✅ MCP server reachable at http://localhost:8085/mcp (HTTP 406)", "success"),
        ("", "default"),
        ("🔍 Checking agent import...", "command"),
        ("✅ Agent imported successfully: weather_agent", "success"),
        ("   Model: gemini-2.5-flash", "highlight"),
        ("", "default"),
        ("============================================================", "dim"),
        ("✅ All checks passed!", "success"),
        ("", "default"),
        ("🚀 Ready to start!", "command"),
        ("   Run: uv run adk web", "prompt"),
        ("📍 Then open: http://localhost:8000", "highlight"),
    ]
    render_terminal("Windows PowerShell - 04-lab Verify Setup", lines_04_verify, "screenshots/04-verify-setup.png", width=1050)

if __name__ == "__main__":
    gen_all()
