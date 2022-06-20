// ignore_for_file: deprecated_member_use, unnecessary_const

import 'package:flutter/material.dart';
import 'auth/login.dart';
import 'interface/home.dart';
import 'auth/register.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

void main() {
  runApp(const Nuclei());
}

class Nuclei extends StatelessWidget {
  const Nuclei({Key? key}) : super(key: key);
  @override
  // check if the user is logged in by checking the local storage

  Widget build(BuildContext context) {
    const storage = const FlutterSecureStorage();
    final token = storage.read(key: "token");
    if (token == null) {
      return const IndexPage();
    } else {
      return const HomePageHandler();
    }
  }
}

class IndexPage extends StatelessWidget {
  const IndexPage({Key? key}) : super(key: key);

  @override
  // check if the user is logged in by checking the local storage

  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          primarySwatch: Colors.purple,
          scaffoldBackgroundColor: Colors.grey[600],
        ),
        home: Builder(
          builder: (context) => Scaffold(
            appBar: AppBar(
              title: const Text('Nuclei'),
            ),
            body: Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  const Text('Nuclei'),
                  const SizedBox(height: 20),
                  RaisedButton(
                    child: const Text('Login'),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const LoginPageView(),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 20),
                  RaisedButton(
                    child: const Text('Register'),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const RegisterPageView(),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        ));
  }
}
