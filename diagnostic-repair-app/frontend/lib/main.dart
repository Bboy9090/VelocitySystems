import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/tickets_screen.dart';
import 'screens/diagnostics_screen.dart';
import 'services/api_service.dart';
import 'services/socket_service.dart';

void main() {
  runApp(const DiagnosticRepairApp());
}

class DiagnosticRepairApp extends StatefulWidget {
  const DiagnosticRepairApp({Key? key}) : super(key: key);

  @override
  State<DiagnosticRepairApp> createState() => _DiagnosticRepairAppState();
}

class _DiagnosticRepairAppState extends State<DiagnosticRepairApp> {
  late ApiService apiService;
  late SocketService socketService;

  @override
  void initState() {
    super.initState();
    apiService = ApiService(baseUrl: 'http://localhost:3000/api');
    socketService = SocketService(serverUrl: 'http://localhost:3000');
    socketService.connect();
  }

  @override
  void dispose() {
    socketService.disconnect();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Diagnostic & Repair',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        brightness: Brightness.light,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
          elevation: 0,
        ),
      ),
      darkTheme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        brightness: Brightness.dark,
      ),
      themeMode: ThemeMode.system,
      initialRoute: '/',
      routes: {
        '/': (context) => HomeScreen(
          apiService: apiService,
          socketService: socketService,
        ),
        '/tickets': (context) => TicketsScreen(
          apiService: apiService,
          socketService: socketService,
        ),
        '/diagnostics': (context) => DiagnosticsScreen(
          apiService: apiService,
          socketService: socketService,
        ),
      },
    );
  }
}
