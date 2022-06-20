// write home page
// Language: dart
// ignore_for_file: use_build_context_synchronously

import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../main.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    const storage = FlutterSecureStorage();
    final token = storage.read(key: "token");
    if (token == null) {
      return const IndexPage();
    } else {
      return Scaffold(
        drawer: Drawer(
          child: ListView(
            children: <Widget>[
              const DrawerHeader(
                decoration: BoxDecoration(
                  color: Colors.purple,
                ),
                child: Text('Nuclei'),
              ),
              ListTile(
                title: const Text('Home'),
                onTap: () {
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: const Text('Profile'),
                onTap: () {
                  Navigator.pop(context);
                },
              ),
              ListTile(
                title: const Text('Logout'),
                onTap: () async {
                  const storage = FlutterSecureStorage();
                  await storage.deleteAll();
                  Navigator.pop(context);
                },
              ),
            ],
          ),
        ),
        appBar: AppBar(
          title: const Text('Nuclei'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: const <Widget>[
              Text('Nuclei'),
            ],
          ),
        ),
      );
    }
  }
}

class HomePageHandler extends StatelessWidget {
  const HomePageHandler({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    const storage = FlutterSecureStorage();
    final token = storage.read(key: "token");
    if (token == null) {
      return const IndexPage();
    } else {
      return MaterialApp(home: HomePage());
    }
  }
}
