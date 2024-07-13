import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<String> readFile(String filePath) async {
  final response =
      await http.get(Uri.parse('http://localhost:3000/file?path=$filePath'));
  if (response.statusCode == 200) {
    return response.body;
  } else {
    throw Exception('Ошибка при чтении файла');
  }
}

Future<void> writeFile(String filePath, String content) async {
  final response = await http.post(
    Uri.parse('http://localhost:3000/file'),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode(<String, String>{
      'path': filePath,
      'content': content,
    }),
  );

  if (response.statusCode != 200) {
    throw Exception('Ошибка при записи в файл');
  }
}

Future<void> toggleBot(bool enable) async {
  final response = await http.post(
    Uri.parse('http://localhost:3000/toggle-bot'),
    headers: {
      'Content-Type': 'application/json',
    },
    body: jsonEncode(<String, bool>{
      'enable': enable,
    }),
  );

  if (response.statusCode != 200) {
    throw Exception('Ошибка при управлении ботом');
  }
}

class FileEditor extends StatefulWidget {
  @override
  _FileEditorState createState() => _FileEditorState();
}

class _FileEditorState extends State<FileEditor> {
  String _selectedFile = '.env';
  TextEditingController _controller = TextEditingController();
  bool _isLoading = false;

  void _loadFile() async {
    setState(() {
      _isLoading = true;
    });

    try {
      String content = await readFile(_selectedFile);
      setState(() {
        _controller.text = content;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка при загрузке файла: $e')));
    }
  }

  void _saveFile() async {
    try {
      await writeFile(_selectedFile, _controller.text);
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('Файл успешно сохранен')));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка при сохранении файла: $e')));
    }
  }

  void _toggleBot(bool enable) async {
    try {
      await toggleBot(enable);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content: Text('Бот успешно ' + (enable ? 'включен' : 'отключен'))));
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка при управлении ботом: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('admin панель'),
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: _saveFile,
          ),
          IconButton(
            icon: Icon(Icons.power_settings_new),
            onPressed: () => _toggleBot(true), // Включить бота
          ),
          IconButton(
            icon: Icon(Icons.power_off),
            onPressed: () => _toggleBot(false), // Выключить бота
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: DropdownButton<String>(
              value: _selectedFile,
              onChanged: (String? newValue) {
                setState(() {
                  _selectedFile = newValue!;
                  _loadFile();
                });
              },
              items: <String>['.env', 'Dockerfile']
                  .map<DropdownMenuItem<String>>((String value) {
                return DropdownMenuItem<String>(
                  value: value,
                  child: Text(value),
                );
              }).toList(),
            ),
          ),
          Expanded(
            child: _isLoading
                ? Center(child: CircularProgressIndicator())
                : Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: TextField(
                      controller: _controller,
                      maxLines: null,
                      expands: true,
                      decoration: InputDecoration(
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}

void main() => runApp(MaterialApp(
      home: FileEditor(),
    ));
