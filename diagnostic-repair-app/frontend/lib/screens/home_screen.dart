import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/socket_service.dart';

class HomeScreen extends StatefulWidget {
  final ApiService apiService;
  final SocketService socketService;

  const HomeScreen({
    Key? key,
    required this.apiService,
    required this.socketService,
  }) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;
  
  final List<Map<String, dynamic>> _menuItems = [
    {
      'title': 'Dashboard',
      'icon': Icons.dashboard,
      'color': Colors.blue,
    },
    {
      'title': 'Repair Tickets',
      'icon': Icons.assignment,
      'color': Colors.orange,
    },
    {
      'title': 'Diagnostics',
      'icon': Icons.health_and_safety,
      'color': Colors.green,
    },
    {
      'title': 'Firmware Flash',
      'icon': Icons.system_update,
      'color': Colors.purple,
    },
    {
      'title': 'QR Scanner',
      'icon': Icons.qr_code_scanner,
      'color': Colors.teal,
    },
    {
      'title': 'Settings',
      'icon': Icons.settings,
      'color': Colors.grey,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Diagnostic & Repair App'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () {
              // Show notifications
            },
          ),
        ],
      ),
      body: _buildBody(),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
          _handleNavigation(index);
        },
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.assignment),
            label: 'Tickets',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.health_and_safety),
            label: 'Diagnostics',
          ),
        ],
      ),
    );
  }

  Widget _buildBody() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Welcome to Diagnostic & Repair',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            'Manage device repairs, run diagnostics, and flash firmware',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 24),
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 2,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.2,
            ),
            itemCount: _menuItems.length,
            itemBuilder: (context, index) {
              final item = _menuItems[index];
              return _buildMenuItem(
                title: item['title'],
                icon: item['icon'],
                color: item['color'],
                onTap: () => _handleNavigation(index),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMenuItem({
    required String title,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Container(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                icon,
                size: 48,
                color: color,
              ),
              const SizedBox(height: 8),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _handleNavigation(int index) {
    switch (index) {
      case 0:
        // Already on home
        break;
      case 1:
        Navigator.pushNamed(context, '/tickets');
        break;
      case 2:
        Navigator.pushNamed(context, '/diagnostics');
        break;
      case 3:
        // Navigate to firmware flash screen
        _showComingSoon('Firmware Flash');
        break;
      case 4:
        // Navigate to QR scanner
        _showComingSoon('QR Scanner');
        break;
      case 5:
        // Navigate to settings
        _showComingSoon('Settings');
        break;
    }
  }

  void _showComingSoon(String feature) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('$feature - Coming Soon!'),
        duration: const Duration(seconds: 2),
      ),
    );
  }
}
