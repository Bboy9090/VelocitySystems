import 'package:socket_io_client/socket_io_client.dart' as IO;

class SocketService {
  final String serverUrl;
  late IO.Socket socket;
  
  final Map<String, Function(dynamic)> _listeners = {};

  SocketService({required this.serverUrl});

  void connect() {
    socket = IO.io(serverUrl, <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': true,
    });

    socket.onConnect((_) {
      print('Connected to Socket.IO server');
    });

    socket.onDisconnect((_) {
      print('Disconnected from Socket.IO server');
    });

    socket.onError((error) {
      print('Socket.IO error: $error');
    });
  }

  void disconnect() {
    socket.disconnect();
    _listeners.clear();
  }

  void subscribeToTicket(String ticketId) {
    socket.emit('subscribe-ticket', ticketId);
  }

  void on(String event, Function(dynamic) callback) {
    _listeners[event] = callback;
    socket.on(event, callback);
  }

  void off(String event) {
    if (_listeners.containsKey(event)) {
      socket.off(event);
      _listeners.remove(event);
    }
  }

  void emit(String event, dynamic data) {
    socket.emit(event, data);
  }

  // Ticket events
  void onTicketCreated(Function(dynamic) callback) {
    on('ticket-created', callback);
  }

  void onTicketUpdated(Function(dynamic) callback) {
    on('ticket-updated', callback);
  }

  void onTicketStatusChanged(Function(dynamic) callback) {
    on('ticket-status-changed', callback);
  }

  void onDiagnosticsUpdated(Function(dynamic) callback) {
    on('diagnostics-updated', callback);
  }

  // Diagnostics events
  void onDiagnosticsStarted(Function(dynamic) callback) {
    on('diagnostics-started', callback);
  }

  void onDiagnosticsCompleted(Function(dynamic) callback) {
    on('diagnostics-completed', callback);
  }

  void onBatteryUpdate(Function(dynamic) callback) {
    on('battery-update', callback);
  }

  // Firmware events
  void onFlashStarted(Function(dynamic) callback) {
    on('flash-started', callback);
  }

  void onFlashProgress(Function(dynamic) callback) {
    on('flash-progress', callback);
  }

  void onFlashCompleted(Function(dynamic) callback) {
    on('flash-completed', callback);
  }

  void onFlashFailed(Function(dynamic) callback) {
    on('flash-failed', callback);
  }

  void onRestoreStarted(Function(dynamic) callback) {
    on('restore-started', callback);
  }

  void onRestoreProgress(Function(dynamic) callback) {
    on('restore-progress', callback);
  }

  void onRestoreCompleted(Function(dynamic) callback) {
    on('restore-completed', callback);
  }

  void onRestoreFailed(Function(dynamic) callback) {
    on('restore-failed', callback);
  }
}
