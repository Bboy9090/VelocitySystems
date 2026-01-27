import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/socket_service.dart';

class DiagnosticsScreen extends StatefulWidget {
  final ApiService apiService;
  final SocketService socketService;

  const DiagnosticsScreen({
    Key? key,
    required this.apiService,
    required this.socketService,
  }) : super(key: key);

  @override
  State<DiagnosticsScreen> createState() => _DiagnosticsScreenState();
}

class _DiagnosticsScreenState extends State<DiagnosticsScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  List<dynamic> _androidDevices = [];
  List<dynamic> _iosDevices = [];
  bool _isLoading = false;
  String? _selectedDeviceId;
  String? _selectedDeviceType;
  Map<String, dynamic>? _diagnosticsData;
  bool _isRunningDiagnostics = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _loadDevices();
    _setupSocketListeners();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _setupSocketListeners() {
    widget.socketService.onDiagnosticsStarted((data) {
      setState(() {
        _isRunningDiagnostics = true;
      });
    });

    widget.socketService.onDiagnosticsCompleted((data) {
      setState(() {
        _isRunningDiagnostics = false;
        if (data['deviceId'] == _selectedDeviceId) {
          _diagnosticsData = data['diagnostics'];
        }
      });
    });

    widget.socketService.onBatteryUpdate((data) {
      if (data['deviceId'] == _selectedDeviceId) {
        setState(() {
          if (_diagnosticsData != null) {
            _diagnosticsData!['battery'] = data['battery'];
          }
        });
      }
    });
  }

  Future<void> _loadDevices() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final androidDevices = await widget.apiService.getAndroidDevices();
      final iosDevices = await widget.apiService.getIOSDevices();

      setState(() {
        _androidDevices = androidDevices;
        _iosDevices = iosDevices;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      _showSnackBar('Error loading devices: $e');
    }
  }

  Future<void> _runDiagnostics() async {
    if (_selectedDeviceId == null || _selectedDeviceType == null) {
      _showSnackBar('Please select a device first');
      return;
    }

    setState(() {
      _isRunningDiagnostics = true;
      _diagnosticsData = null;
    });

    try {
      Map<String, dynamic> diagnostics;
      if (_selectedDeviceType == 'android') {
        diagnostics = await widget.apiService.runAndroidDiagnostics(_selectedDeviceId!);
      } else {
        diagnostics = await widget.apiService.runIOSDiagnostics(_selectedDeviceId!);
      }

      setState(() {
        _diagnosticsData = diagnostics;
        _isRunningDiagnostics = false;
      });
    } catch (e) {
      setState(() {
        _isRunningDiagnostics = false;
      });
      _showSnackBar('Error running diagnostics: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Device Diagnostics'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Android', icon: Icon(Icons.android)),
            Tab(text: 'iOS', icon: Icon(Icons.apple)),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadDevices,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : TabBarView(
              controller: _tabController,
              children: [
                _buildDeviceList(_androidDevices, 'android'),
                _buildDeviceList(_iosDevices, 'ios'),
              ],
            ),
      floatingActionButton: _selectedDeviceId != null
          ? FloatingActionButton.extended(
              onPressed: _isRunningDiagnostics ? null : _runDiagnostics,
              icon: _isRunningDiagnostics
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Icon(Icons.play_arrow),
              label: Text(_isRunningDiagnostics ? 'Running...' : 'Run Diagnostics'),
            )
          : null,
    );
  }

  Widget _buildDeviceList(List<dynamic> devices, String deviceType) {
    if (devices.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              deviceType == 'android' ? Icons.android : Icons.apple,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: 16),
            Text('No ${deviceType.toUpperCase()} devices connected'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadDevices,
              child: const Text('Refresh'),
            ),
          ],
        ),
      );
    }

    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: devices.length,
            itemBuilder: (context, index) {
              final device = devices[index];
              final isSelected = _selectedDeviceId == device['id'];

              return Card(
                color: isSelected
                    ? Theme.of(context).primaryColor.withOpacity(0.1)
                    : null,
                child: ListTile(
                  leading: Icon(
                    deviceType == 'android' ? Icons.android : Icons.apple,
                    color: isSelected ? Theme.of(context).primaryColor : null,
                  ),
                  title: Text(device['id'] ?? 'Unknown'),
                  subtitle: Text('Type: ${device['type'] ?? 'N/A'}'),
                  trailing: isSelected
                      ? const Icon(Icons.check_circle, color: Colors.green)
                      : null,
                  onTap: () {
                    setState(() {
                      _selectedDeviceId = device['id'];
                      _selectedDeviceType = deviceType;
                      _diagnosticsData = null;
                    });
                  },
                ),
              );
            },
          ),
        ),
        if (_diagnosticsData != null) _buildDiagnosticsResults(),
      ],
    );
  }

  Widget _buildDiagnosticsResults() {
    return Container(
      constraints: BoxConstraints(
        maxHeight: MediaQuery.of(context).size.height * 0.5,
      ),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Diagnostics Results',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () {
                    setState(() {
                      _diagnosticsData = null;
                    });
                  },
                ),
              ],
            ),
            const Divider(),
            const SizedBox(height: 8),
            if (_diagnosticsData!['battery'] != null)
              _buildDiagnosticCard(
                'Battery',
                Icons.battery_full,
                _diagnosticsData!['battery'],
              ),
            if (_diagnosticsData!['storage'] != null)
              _buildDiagnosticCard(
                'Storage',
                Icons.storage,
                _diagnosticsData!['storage'],
              ),
            if (_diagnosticsData!['memory'] != null)
              _buildDiagnosticCard(
                'Memory',
                Icons.memory,
                _diagnosticsData!['memory'],
              ),
            if (_diagnosticsData!['cpu'] != null)
              _buildDiagnosticCard(
                'CPU',
                Icons.developer_board,
                _diagnosticsData!['cpu'],
              ),
            if (_diagnosticsData!['network'] != null)
              _buildDiagnosticCard(
                'Network',
                Icons.network_check,
                _diagnosticsData!['network'],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildDiagnosticCard(String title, IconData icon, Map<String, dynamic> data) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Theme.of(context).primaryColor),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            ...data.entries.map((entry) {
              if (entry.value is Map) {
                return Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Text(
                    '${entry.key}: [Complex data]',
                    style: const TextStyle(fontSize: 14),
                  ),
                );
              }
              return Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      '${entry.key}:',
                      style: const TextStyle(fontWeight: FontWeight.w500),
                    ),
                    Text(entry.value.toString()),
                  ],
                ),
              );
            }).toList(),
          ],
        ),
      ),
    );
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}
