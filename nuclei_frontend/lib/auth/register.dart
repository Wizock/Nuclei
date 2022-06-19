import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'dart:async';
import '../main.dart';

class RegisterPageForm extends StatelessWidget {
  const RegisterPageForm({Key? key}) : super(key: key);
  static final TextEditingController _usernameController =
      TextEditingController();
  static final TextEditingController _passwordController =
      TextEditingController();
  static final TextEditingController _emailController = TextEditingController();
  @override
  Widget build(BuildContext context) {
    final _formKey = GlobalKey<FormState>();

    final ButtonStyle raisedButtonStyle = ElevatedButton.styleFrom(
      onPrimary: Colors.black87,
      primary: Colors.grey[300],
      // add a bit of margin on left and right but limit the height
      minimumSize: const Size(
        double.infinity,
        60,
      ),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(Radius.circular(2)),
      ),
    );
    return Form(
      key: _formKey,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          // write a form
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email',
              labelStyle: TextStyle(
                fontSize: 15,
                color: Colors.white,
                // add a darker shade of white
              ),
              hintText: "At least 6 characters",
            ),
            style: const TextStyle(
              fontSize: 20,
              // add a shade of color
              color: Colors.white,
            ),
          ),
          TextFormField(
            controller: _usernameController,
            decoration: const InputDecoration(
              labelText: 'Username',
              labelStyle: TextStyle(
                fontSize: 15,
                color: Colors.white,
                // add a darker shade of white
              ),
              hintText: "At least 6 characters",
            ),
            style: const TextStyle(
              fontSize: 20,
              // add a shade of color
              color: Colors.white,
            ),
          ),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(
              labelText: 'password',
              labelStyle: TextStyle(
                fontSize: 15,
                color: Colors.white,
              ),
              hintText: "At least 6 characters",
            ),
            style: const TextStyle(
              fontSize: 20,
              color: Colors.white,
            ),
          ),

          ElevatedButton(
              style: raisedButtonStyle,
              onPressed: () async {
                var response = await post(
                  Uri.parse("http://10.1.1.41:5000/auth/register"),
                  body: json.encode({
                    "email": _emailController.text,
                    "password": _passwordController.text,
                    "username": _usernameController.text,
                  }),
                  headers: {
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                  },
                );
              },
              child: const Text('Login')),
        ],
      ),
    );
  }
}

class RegisterPageView extends StatelessWidget {
  const RegisterPageView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(),
        body: const Center(
          child: RegisterPageForm(),
        ));
  }
}
