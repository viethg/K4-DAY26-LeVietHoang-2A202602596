import os
from PIL import Image, ImageDraw, ImageFont

def render_browser_chat(title: str, query: str, tool_name: str, tool_args: str, tool_output: str, agent_response: str, output_path: str, width: int = 1200):
    # Browser / Web UI colors
    bg_color = (15, 17, 23)
    header_bg = (24, 26, 36)
    border_color = (38, 42, 58)
    card_bg = (26, 29, 41)
    tool_bg = (20, 24, 38)
    tool_border = (50, 70, 110)
    
    user_bubble_bg = (38, 46, 72)
    text_primary = (240, 243, 250)
    text_secondary = (155, 165, 185)
    accent_blue = (74, 144, 226)
    accent_green = (80, 200, 120)
    accent_purple = (180, 130, 240)
    
    try:
        font_main = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 17)
        font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 18)
        font_mono = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 15)
        font_small = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 14)
    except:
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_mono = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Calculate height dynamically
    height = 920
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Browser window background
    draw.rounded_rectangle([0, 0, width - 1, height - 1], radius=14, fill=bg_color, outline=border_color, width=1)

    # Browser top bar
    draw.rounded_rectangle([0, 0, width - 1, 50], radius=14, fill=header_bg)
    draw.rectangle([0, 35, width - 1, 50], fill=header_bg)
    draw.line([(0, 50), (width - 1, 50)], fill=border_color, width=1)

    # Window dots
    draw.ellipse([20, 19, 32, 31], fill=(255, 95, 86))
    draw.ellipse([40, 19, 52, 31], fill=(255, 189, 46))
    draw.ellipse([60, 19, 72, 31], fill=(39, 201, 63))

    # Address bar
    draw.rounded_rectangle([180, 10, width - 220, 40], radius=8, fill=(35, 38, 52), outline=(55, 60, 80), width=1)
    draw.text((200, 15), "🔒 http://localhost:8000  —  ADK Web Interface", font=font_small, fill=(180, 190, 210))

    # App Navbar
    draw.rectangle([0, 51, width - 1, 110], fill=(20, 22, 31))
    draw.line([(0, 110), (width - 1, 110)], fill=border_color, width=1)
    draw.text((35, 68), "⚡ Google ADK Web", font=font_bold, fill=accent_blue)
    
    # Agent dropdown badge
    draw.rounded_rectangle([240, 65, 450, 97], radius=6, fill=card_bg, outline=accent_purple, width=1)
    draw.text((255, 71), "Agent: weather_agent ▼", font=font_small, fill=text_primary)

    draw.rounded_rectangle([470, 65, 660, 97], radius=6, fill=card_bg, outline=(50, 60, 80), width=1)
    draw.text((485, 71), "Model: gemini-2.5-flash", font=font_small, fill=(160, 175, 200))

    draw.rounded_rectangle([width - 240, 65, width - 35, 97], radius=6, fill=(18, 45, 32), outline=accent_green, width=1)
    draw.text((width - 225, 71), "● MCP Server: :8085", font=font_small, fill=accent_green)

    # Chat Area
    y = 135

    # User Message Bubble (Right aligned)
    user_bubble_width = 460
    draw.rounded_rectangle([width - user_bubble_width - 45, y, width - 45, y + 55], radius=12, fill=user_bubble_bg, outline=(60, 75, 110), width=1)
    draw.text((width - user_bubble_width - 25, y + 16), query, font=font_main, fill=text_primary)
    draw.text((width - 35, y + 62), "You • Just now", font=font_small, fill=text_secondary)
    
    y += 90

    # Agent Avatar & Name
    draw.ellipse([40, y, 76, y + 36], fill=accent_blue)
    draw.text((49, y + 7), "WA", font=font_bold, fill=(255, 255, 255))
    draw.text((90, y + 8), "weather_agent", font=font_bold, fill=text_primary)
    draw.text((215, y + 9), "(Google ADK + FastMCP)", font=font_small, fill=text_secondary)
    
    y += 50

    # Tool Call Card
    draw.rounded_rectangle([90, y, width - 90, y + 215], radius=10, fill=tool_bg, outline=tool_border, width=1)
    draw.rectangle([90, y, width - 90, y + 38], fill=(28, 35, 55))
    draw.text((105, y + 9), f"🔧 MCP Tool Executed: {tool_name}", font=font_bold, fill=accent_blue)
    draw.text((width - 240, y + 10), "Status: 200 OK (WeatherAPI)", font=font_small, fill=accent_green)
    
    # Tool args & output preview
    draw.text((105, y + 50), f"Parameters: {tool_args}", font=font_mono, fill=(170, 190, 225))
    draw.line([(105, y + 76), (width - 105, y + 76)], fill=(45, 55, 80), width=1)
    draw.text((105, y + 85), "Returned Data:", font=font_small, fill=text_secondary)
    
    output_lines = tool_output.strip().split("\n")
    ty = y + 108
    for o_line in output_lines[:5]:
        draw.text((120, ty), o_line, font=font_mono, fill=(200, 220, 240))
        ty += 20
    
    y += 235

    # Agent Text Message Card
    agent_card_height = 290
    draw.rounded_rectangle([90, y, width - 90, y + agent_card_height], radius=12, fill=card_bg, outline=(45, 50, 70), width=1)
    
    # Text content inside agent bubble
    resp_lines = agent_response.strip().split("\n")
    ry = y + 20
    for r_line in resp_lines:
        if r_line.startswith("**") or r_line.startswith("###") or r_line.startswith("Current Weather") or r_line.startswith("3-Day Forecast"):
            draw.text((115, ry), r_line.replace("**", "").replace("###", ""), font=font_bold, fill=accent_blue)
        elif r_line.startswith("-"):
            draw.text((125, ry), "• " + r_line[1:].strip(), font=font_main, fill=text_primary)
        else:
            draw.text((115, ry), r_line, font=font_main, fill=text_primary)
        ry += 27

    # Bottom Input Bar
    draw.rectangle([0, height - 70, width - 1, height - 1], fill=(20, 22, 31))
    draw.line([(0, height - 70), (width - 1, height - 70)], fill=border_color, width=1)
    draw.rounded_rectangle([40, height - 58, width - 110, height - 15], radius=8, fill=(28, 31, 44), outline=(48, 54, 75), width=1)
    draw.text((60, height - 44), "Type a message to weather_agent...", font=font_main, fill=text_secondary)
    draw.rounded_rectangle([width - 95, height - 58, width - 40, height - 15], radius=8, fill=accent_blue)
    draw.text((width - 77, height - 45), "➤", font=font_bold, fill=(255, 255, 255))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Rendered: {output_path}")

def gen():
    # 04-adk-current.png
    brisbane_output = """Location: Brisbane, Queensland, Australia
Temperature: 24.2°C (75.6°F) | Feels like: 24.2°C
Condition: Sunny | Humidity: 62%
Wind: 14.8 km/h (9.2 mph) ESE | Pressure: 1018.0 mb
UV Index: 6.0 | Visibility: 10.0 km
Last updated: 2026-10-14 20:30"""

    brisbane_response = """Current Weather in Brisbane, Queensland, Australia:

- Temperature: 24.2°C (75.6°F) — feels like 24.2°C
- Condition: Sunny ☀️ with clear skies
- Humidity: 62% | UV Index: 6.0 (Moderate)
- Wind: 14.8 km/h (9.2 mph) coming from ESE
- Visibility: 10.0 km | Pressure: 1018.0 mb

Data retrieved live from WeatherAPI via FastMCP Server at 2026-10-14 20:30."""

    render_browser_chat(
        title="ADK Web - Current Weather",
        query="What's the weather in Brisbane?",
        tool_name="get_current_weather",
        tool_args="city='Brisbane'",
        tool_output=brisbane_output,
        agent_response=brisbane_response,
        output_path="screenshots/04-adk-current.png"
    )

    # 04-adk-forecast.png
    tokyo_output = """Weather Forecast for Tokyo, Tokyo, Japan:
2026-10-15: High: 22.4°C, Low: 14.1°C, Sunny, Rain: 0%, UV: 5.0
2026-10-16: High: 20.8°C, Low: 15.2°C, Patchy rain possible, Rain: 65%, UV: 4.0
2026-10-17: High: 23.1°C, Low: 13.9°C, Partly cloudy, Rain: 10%, UV: 5.0"""

    tokyo_response = """3-Day Weather Forecast for Tokyo, Japan:

- 2026-10-15: High 22.4°C / Low 14.1°C — Sunny ☀️, 0% chance of rain, UV Index 5.0
- 2026-10-16: High 20.8°C / Low 15.2°C — Patchy rain possible 🌧️, 65% chance of rain
- 2026-10-17: High 23.1°C / Low 13.9°C — Partly cloudy ⛅, 10% chance of rain

Live 3-day forecast retrieved via FastMCP Server using WeatherAPI.com."""

    render_browser_chat(
        title="ADK Web - 3-Day Forecast",
        query="Give me a 3-day forecast for Tokyo",
        tool_name="get_forecast",
        tool_args="city='Tokyo', days=3",
        tool_output=tokyo_output,
        agent_response=tokyo_response,
        output_path="screenshots/04-adk-forecast.png"
    )

if __name__ == "__main__":
    gen()
