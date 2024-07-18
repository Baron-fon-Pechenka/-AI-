const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const { spawn } = require("child_process");
const psTree = require("ps-tree");
require("dotenv").config({ path: path.join(__dirname, "../../.env") });

const app = express();
const port = 443;

app.use(express.json());
app.use(cors());

const rootPath = path.resolve(__dirname, "../..");

app.get("/file", (req, res) => {
  const filePath = path.join(rootPath, req.query.path);
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      res.status(500).send("Ошибка при чтении файла");
    } else {
      res.send(data);
    }
  });
});

app.post("/file", (req, res) => {
  const filePath = path.join(rootPath, req.body.path);
  const content = req.body.content;
  fs.writeFile(filePath, content, "utf8", (err) => {
    if (err) {
      res.status(500).send("Ошибка при записи в файл");
    } else {
      res.send("Файл успешно сохранен");
    }
  });
});

let botProcess = null;

app.post("/toggle-bot", (req, res) => {
  const enable = req.body.enable;
  const botScriptPath = path.resolve(__dirname, "tgbot.py");
  const pythonPath =
    "C:/Users/yuraa/AppData/Local/Programs/Python/Python310/python.exe"; // замените на путь к вашему интерпретатору Python

  if (enable) {
    if (botProcess) {
      return res.send("Бот уже запущен");
    }
    console.log(`Запуск команды: ${pythonPath} ${botScriptPath}`);
    botProcess = spawn(pythonPath, [botScriptPath], { detached: true });

    botProcess.stdout.on("data", (data) => {
      console.log(`stdout: ${data}`);
    });

    botProcess.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    botProcess.on("close", (code) => {
      console.log(`Процесс завершился с кодом: ${code}`);
      botProcess = null;
    });

    res.send("Бот успешно запущен");
  } else {
    if (!botProcess) {
      return res.send("Бот не запущен");
    }

    console.log("Остановка бота");

    psTree(botProcess.pid, (err, children) => {
      if (err) {
        console.error("Ошибка при получении списка дочерних процессов:", err);
        return res.status(500).send("Ошибка при остановке бота");
      }

      [botProcess.pid].concat(children.map((p) => p.PID)).forEach((tpid) => {
        try {
          process.kill(tpid);
        } catch (err) {
          if (err.code !== "ESRCH") {
            console.error(`Ошибка при завершении процесса ${tpid}:`, err);
          }
        }
      });

      botProcess = null;
      res.send("Бот успешно остановлен");
    });
  }
});

app.listen(port, () => {
  console.log(`Сервер запущен на порту ${port}`);
});
