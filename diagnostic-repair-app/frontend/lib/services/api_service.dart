import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({required this.baseUrl});

  // Tickets API
  Future<List<dynamic>> getTickets({String? status, String? customerId}) async {
    String url = '$baseUrl/tickets';
    List<String> queryParams = [];
    
    if (status != null) queryParams.add('status=$status');
    if (customerId != null) queryParams.add('customerId=$customerId');
    
    if (queryParams.isNotEmpty) {
      url += '?${queryParams.join('&')}';
    }

    final response = await http.get(Uri.parse(url));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['tickets'];
    } else {
      throw Exception('Failed to load tickets');
    }
  }

  Future<Map<String, dynamic>> getTicket(String ticketId) async {
    final response = await http.get(Uri.parse('$baseUrl/tickets/$ticketId'));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['ticket'];
    } else {
      throw Exception('Failed to load ticket');
    }
  }

  Future<Map<String, dynamic>> createTicket(Map<String, dynamic> ticketData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/tickets'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(ticketData),
    );
    
    if (response.statusCode == 201) {
      final data = json.decode(response.body);
      return data['ticket'];
    } else {
      throw Exception('Failed to create ticket');
    }
  }

  Future<Map<String, dynamic>> updateTicket(String ticketId, Map<String, dynamic> updates) async {
    final response = await http.put(
      Uri.parse('$baseUrl/tickets/$ticketId'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(updates),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['ticket'];
    } else {
      throw Exception('Failed to update ticket');
    }
  }

  Future<Map<String, dynamic>> updateTicketStatus(
    String ticketId, 
    String status, 
    {String? note}
  ) async {
    final response = await http.patch(
      Uri.parse('$baseUrl/tickets/$ticketId/status'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'status': status, 'note': note}),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['ticket'];
    } else {
      throw Exception('Failed to update ticket status');
    }
  }

  // Android Diagnostics API
  Future<List<dynamic>> getAndroidDevices() async {
    final response = await http.get(Uri.parse('$baseUrl/android/devices'));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['devices'];
    } else {
      throw Exception('Failed to load Android devices');
    }
  }

  Future<Map<String, dynamic>> getAndroidDeviceInfo(String deviceId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/android/devices/$deviceId/info')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['device'];
    } else {
      throw Exception('Failed to load device info');
    }
  }

  Future<Map<String, dynamic>> getAndroidBattery(String deviceId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/android/devices/$deviceId/battery')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['battery'];
    } else {
      throw Exception('Failed to load battery info');
    }
  }

  Future<Map<String, dynamic>> runAndroidDiagnostics(String deviceId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/android/devices/$deviceId/diagnostics')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['diagnostics'];
    } else {
      throw Exception('Failed to run diagnostics');
    }
  }

  // iOS Diagnostics API
  Future<List<dynamic>> getIOSDevices() async {
    final response = await http.get(Uri.parse('$baseUrl/ios/devices'));
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['devices'];
    } else {
      throw Exception('Failed to load iOS devices');
    }
  }

  Future<Map<String, dynamic>> getIOSDeviceInfo(String deviceId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/ios/devices/$deviceId/info')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['device'];
    } else {
      throw Exception('Failed to load device info');
    }
  }

  Future<Map<String, dynamic>> getIOSBattery(String deviceId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/ios/devices/$deviceId/battery')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['battery'];
    } else {
      throw Exception('Failed to load battery info');
    }
  }

  Future<Map<String, dynamic>> runIOSDiagnostics(String deviceId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/ios/devices/$deviceId/diagnostics')
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['diagnostics'];
    } else {
      throw Exception('Failed to run diagnostics');
    }
  }

  // Firmware API
  Future<Map<String, dynamic>> flashAndroidFirmware({
    required String deviceId,
    required String firmwarePath,
    required String partition,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/firmware/android/flash'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'deviceId': deviceId,
        'firmwarePath': firmwarePath,
        'partition': partition,
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to start firmware flash');
    }
  }

  Future<Map<String, dynamic>> restoreIOS({
    required String deviceId,
    required String ipswPath,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/firmware/ios/restore'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'deviceId': deviceId,
        'ipswPath': ipswPath,
      }),
    );
    
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to start iOS restore');
    }
  }
}
