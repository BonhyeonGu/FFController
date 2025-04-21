import json
import psutil
import subprocess
import time
from datetime import datetime
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
jsonPath = './proc.json'


def readJson():
    with open(jsonPath, 'r', encoding='utf-8') as f:
        return json.load(f)


def writeJson(data):
    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def procFind(cmd: str):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'ffmpeg' and ' '.join(proc.info['cmdline']) == cmd:
                return proc.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def procKill(pid):
    try:
        if psutil.pid_exists(pid):
            p = psutil.Process(pid)
            p.terminate()
            p.wait(timeout=5)
            print(f"[INFO] Terminated process PID {pid}")
    except Exception as e:
        print(f"[ERROR] Failed to kill process {pid}: {e}")


def procStart(cmd):
    proc = subprocess.Popen(cmd, shell=True)
    print(f"[INFO] Started process PID {proc.pid} with command:\n  {cmd}")
    return proc.pid


def procRestart(cmd, oldPid=None):
    if oldPid:
        procKill(oldPid)
    return procStart(cmd)


def procCheckAllAlive(data):
    changed = False
    for entry in data["proc"]:
        cmd = entry["cmd"]
        pid = entry.get("pid")
        alive = psutil.pid_exists(pid) if pid else False
        foundPid = procFind(cmd)
        if not alive or not foundPid:
            print(f"[WARN] Process dead. Restarting:\n  {cmd}")
            newPid = procStart(cmd)
            entry["pid"] = newPid
            changed = True
    return changed


@app.route('/', methods=['GET', 'POST'])
def index():
    data = readJson()

    # 상태 확인 추가
    for entry in data["proc"]:
        pid = entry.get("pid")
        alive = psutil.pid_exists(pid) if pid else False
        found = procFind(entry["cmd"])
        entry["status"] = "RUNNING" if alive and found else "DEAD"

    if request.method == 'POST':
        if 'cmd' in request.form:
            newCmd = request.form['cmd']
            pid = procStart(newCmd)
            data["proc"].append({"cmd": newCmd, "pid": pid, "status": "RUNNING"})
            writeJson(data)
        elif 'delete_index' in request.form:
            idx = int(request.form['delete_index'])
            procKill(data["proc"][idx].get("pid"))
            del data["proc"][idx]
            writeJson(data)
        return redirect('/')

    return renderTemplate(data)


def renderTemplate(data):
    return render_template("index.html", data=data["proc"])


@app.route('/health')
def healthCheck():
    data = readJson()
    changed = procCheckAllAlive(data)
    if changed:
        writeJson(data)
    return {"status": "checked", "updated": changed}


def runningTime(timeRunning):
    days = timeRunning.days
    seconds = timeRunning.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return f"{days}:{hours}:{minutes}:{seconds}"


def autoRestartLoop():
    data = readJson()
    reHour = int(data["reTime"]["hour"])
    reMin = int(data["reTime"]["min"])
    delayMin = int(data["reTime"]["delayMin"])
    reMinPlus = reMin + delayMin
    swNeedRestart = True
    timeStart = datetime.now()

    for entry in data["proc"]:
        entry["pid"] = procStart(entry["cmd"])
    writeJson(data)

    while True:
        now = datetime.now()

        if procCheckAllAlive(data):
            writeJson(data)

        if now.hour == reHour:
            if now.minute == reMin and swNeedRestart:
                print(f"\n[INFO] Scheduled full restart triggered.")
                for entry in data["proc"]:
                    entry["pid"] = procRestart(entry["cmd"], entry.get("pid"))
                writeJson(data)
                swNeedRestart = False
                print(f"[INFO] Running Time: {runningTime(now - timeStart)}\n")
            elif now.minute == reMinPlus:
                swNeedRestart = True

        time.sleep(5)  # 5초 간격 감시


if __name__ == '__main__':
    import threading
    threading.Thread(target=autoRestartLoop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
