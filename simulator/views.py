from django.shortcuts import render, redirect
from datetime import datetime

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT')

        with open("logs.txt", "a") as f:
            f.write(
                f"{datetime.now()} | "
                f"IP={ip_address} | "
                f"EMAIL={email} | "
                f"UA={user_agent}\n"
            )

        return redirect("warning")

    return render(request, "login.html")


def warning_view(request):
    is_analyst = request.GET.get("analyst") == "true"
    return render(request, "warning.html", {"is_analyst": is_analyst})



def soc_dashboard(request):
    events = []

    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            parts = line.strip().split(" | ")
            if len(parts) >= 4:
                events.append({
                    "id": index,
                    "time": parts[0],
                    "ip": parts[1].replace("IP=", ""),
                    "email": parts[2].replace("EMAIL=", ""),
                    "ua": parts[3].replace("UA=", ""),
                })
    except FileNotFoundError:
        pass

    return render(request, "soc_dashboard.html", {"events": events})
def delete_log(request, log_id):
    try:
        with open("logs.txt", "r") as f:
            lines = f.readlines()

        if 0 <= log_id < len(lines):
            del lines[log_id]

        with open("logs.txt", "w") as f:
            f.writelines(lines)

    except FileNotFoundError:
        pass

    return redirect("soc")
