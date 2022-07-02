import 'package:supabase_flutter/supabase_flutter.dart';

// https://supabase.com/docs/reference/dart/auth-signinwithprovider
class creds {
  static const String anon_key =
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNxY2FvYWNmY29leXZhcW1hZ3pnIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NTY3NjkzODAsImV4cCI6MTk3MjM0NTM4MH0.vGkecfF4U1Rh_EUP6F7nTQ5CKC-8n50laoW3TZMgTjQ";
  static const String url = "https://sqcaoacfcoeyvaqmagzg.supabase.co";
}

Future<int> login_users(String email, String password) async {
  final supabase =
      await Supabase.initialize(url: creds.url, anonKey: creds.anon_key);
  final user = await supabase.auth.signIn(email: email, password: password);
  return user.id;
}
