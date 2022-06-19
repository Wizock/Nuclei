// ignore_for_file: deprecated_member_use, unnecessary_const

import 'package:flutter/material.dart';
import 'auth/login.dart';
import 'auth/register.dart';

void main() {
  runApp(const IndexPage());
}

class IndexPage extends StatelessWidget {
  const IndexPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.purple,
        scaffoldBackgroundColor: Colors.grey[850],
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
                  Navigator.pushNamed(
                    context,
                    '/login',
                  );
                },
              ),
              const SizedBox(height: 20),
              RaisedButton(
                child: const Text('Register'),
                onPressed: () {
                  Navigator.pushNamed(
                    context,
                    '/register',
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
