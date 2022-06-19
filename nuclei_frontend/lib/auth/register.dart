import 'package:flutter/material.dart';

import 'package:flutter/material.dart';
import '../main.dart';

class RegisterPage extends StatelessWidget {
  const RegisterPage({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Center(
        child: FlatButton(
          child: Text('View Details'),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
      ),
    );
  }
}
