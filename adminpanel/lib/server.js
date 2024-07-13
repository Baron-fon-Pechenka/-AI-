const express = require("express");
const fs = require("fs");
const path = require("path");
const cors = require("cors");
const axios = require("axios");
require("dotenv").config({ path: path.join(__dirname, "../../.env") });

const app = express();
const port = 443; // Изменяем порт на 443

app.use(express.json());
app.use(cors());

const botToken = process.env.BOT_TOKEN;
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

app.post("/toggle-bot", async (req, res) => {
  const enable = req.body.enable;

  if (!botToken) {
    return res.status(500).send("Отсутствует токен бота в .env");
  }

  try {
    const response = await axios.post(
      `https://api.telegram.org/bot${botToken}/setWebhook`,
      {
        url: `https://${req.hostname}:${port}/webhook`, // Пример: https://example.com/webhook
      }
    );
    console.log("Ответ от Telegram API:", response.data);
    res.send("Бот успешно настроен");
  } catch (error) {
    console.error("Ошибка при настройке бота:", error.message);
    console.log("Ответ от Telegram API:", error.response.data);
    res.status(500).send("Ошибка при настройке бота");
  }
});

app.listen(port, () => {
  console.log(`Сервер запущен на порту ${port}`);
});
