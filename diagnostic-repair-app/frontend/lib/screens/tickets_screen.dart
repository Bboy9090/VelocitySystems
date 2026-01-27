import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/socket_service.dart';

class TicketsScreen extends StatefulWidget {
  final ApiService apiService;
  final SocketService socketService;

  const TicketsScreen({
    Key? key,
    required this.apiService,
    required this.socketService,
  }) : super(key: key);

  @override
  State<TicketsScreen> createState() => _TicketsScreenState();
}

class _TicketsScreenState extends State<TicketsScreen> {
  List<dynamic> _tickets = [];
  bool _isLoading = false;
  String? _errorMessage;
  String _selectedStatus = 'all';

  @override
  void initState() {
    super.initState();
    _loadTickets();
    _setupSocketListeners();
  }

  void _setupSocketListeners() {
    widget.socketService.onTicketCreated((data) {
      setState(() {
        _tickets.insert(0, data);
      });
      _showSnackBar('New ticket created');
    });

    widget.socketService.onTicketUpdated((data) {
      setState(() {
        final index = _tickets.indexWhere((t) => t['id'] == data['id']);
        if (index != -1) {
          _tickets[index] = data;
        }
      });
    });
  }

  Future<void> _loadTickets() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final status = _selectedStatus == 'all' ? null : _selectedStatus;
      final tickets = await widget.apiService.getTickets(status: status);
      setState(() {
        _tickets = tickets;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Repair Tickets'),
        actions: [
          PopupMenuButton<String>(
            onSelected: (value) {
              setState(() {
                _selectedStatus = value;
              });
              _loadTickets();
            },
            itemBuilder: (context) => [
              const PopupMenuItem(value: 'all', child: Text('All Tickets')),
              const PopupMenuItem(value: 'open', child: Text('Open')),
              const PopupMenuItem(value: 'in-progress', child: Text('In Progress')),
              const PopupMenuItem(value: 'completed', child: Text('Completed')),
            ],
          ),
        ],
      ),
      body: _buildBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: _showCreateTicketDialog,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_errorMessage != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text('Error: $_errorMessage'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadTickets,
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }

    if (_tickets.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.assignment, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            const Text('No tickets found'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _showCreateTicketDialog,
              child: const Text('Create Ticket'),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _loadTickets,
      child: ListView.builder(
        itemCount: _tickets.length,
        padding: const EdgeInsets.all(16),
        itemBuilder: (context, index) {
          final ticket = _tickets[index];
          return _buildTicketCard(ticket);
        },
      ),
    );
  }

  Widget _buildTicketCard(Map<String, dynamic> ticket) {
    final status = ticket['status'] ?? 'unknown';
    final statusColor = _getStatusColor(status);

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: () => _showTicketDetails(ticket),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    ticket['ticketNumber'] ?? 'N/A',
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: statusColor.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      status.toUpperCase(),
                      style: TextStyle(
                        color: statusColor,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                'Customer: ${ticket['customer']?['name'] ?? 'N/A'}',
                style: const TextStyle(fontSize: 14),
              ),
              const SizedBox(height: 4),
              Text(
                'Device: ${ticket['device']?['manufacturer'] ?? 'N/A'} ${ticket['device']?['model'] ?? 'N/A'}',
                style: const TextStyle(fontSize: 14),
              ),
              const SizedBox(height: 4),
              Text(
                'Issue: ${ticket['issue']?['description'] ?? 'N/A'}',
                style: const TextStyle(fontSize: 14),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'open':
        return Colors.blue;
      case 'in-progress':
        return Colors.orange;
      case 'completed':
        return Colors.green;
      case 'cancelled':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  void _showTicketDetails(Map<String, dynamic> ticket) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        expand: false,
        builder: (context, scrollController) {
          return Container(
            padding: const EdgeInsets.all(16),
            child: ListView(
              controller: scrollController,
              children: [
                Text(
                  ticket['ticketNumber'] ?? 'N/A',
                  style: const TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                _buildDetailRow('Status', ticket['status'] ?? 'N/A'),
                _buildDetailRow('Customer', ticket['customer']?['name'] ?? 'N/A'),
                _buildDetailRow('Email', ticket['customer']?['email'] ?? 'N/A'),
                _buildDetailRow('Phone', ticket['customer']?['phone'] ?? 'N/A'),
                const Divider(height: 32),
                _buildDetailRow('Device Type', ticket['device']?['type'] ?? 'N/A'),
                _buildDetailRow('Manufacturer', ticket['device']?['manufacturer'] ?? 'N/A'),
                _buildDetailRow('Model', ticket['device']?['model'] ?? 'N/A'),
                _buildDetailRow('Serial', ticket['device']?['serialNumber'] ?? 'N/A'),
                const Divider(height: 32),
                _buildDetailRow('Issue', ticket['issue']?['description'] ?? 'N/A'),
                _buildDetailRow('Category', ticket['issue']?['category'] ?? 'N/A'),
                _buildDetailRow('Severity', ticket['issue']?['severity'] ?? 'N/A'),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                    _showUpdateStatusDialog(ticket);
                  },
                  child: const Text('Update Status'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 120,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          Expanded(
            child: Text(value),
          ),
        ],
      ),
    );
  }

  void _showCreateTicketDialog() {
    final nameController = TextEditingController();
    final emailController = TextEditingController();
    final phoneController = TextEditingController();
    final manufacturerController = TextEditingController();
    final modelController = TextEditingController();
    final issueController = TextEditingController();
    String deviceType = 'android';

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Create New Ticket'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: 'Customer Name'),
              ),
              TextField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              TextField(
                controller: phoneController,
                decoration: const InputDecoration(labelText: 'Phone'),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                value: deviceType,
                decoration: const InputDecoration(labelText: 'Device Type'),
                items: const [
                  DropdownMenuItem(value: 'android', child: Text('Android')),
                  DropdownMenuItem(value: 'ios', child: Text('iOS')),
                ],
                onChanged: (value) {
                  deviceType = value ?? 'android';
                },
              ),
              TextField(
                controller: manufacturerController,
                decoration: const InputDecoration(labelText: 'Manufacturer'),
              ),
              TextField(
                controller: modelController,
                decoration: const InputDecoration(labelText: 'Model'),
              ),
              TextField(
                controller: issueController,
                decoration: const InputDecoration(labelText: 'Issue Description'),
                maxLines: 3,
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await widget.apiService.createTicket({
                  'customer': {
                    'name': nameController.text,
                    'email': emailController.text,
                    'phone': phoneController.text,
                  },
                  'device': {
                    'type': deviceType,
                    'manufacturer': manufacturerController.text,
                    'model': modelController.text,
                  },
                  'issue': {
                    'description': issueController.text,
                  },
                });
                Navigator.pop(context);
                _loadTickets();
                _showSnackBar('Ticket created successfully');
              } catch (e) {
                _showSnackBar('Error creating ticket: $e');
              }
            },
            child: const Text('Create'),
          ),
        ],
      ),
    );
  }

  void _showUpdateStatusDialog(Map<String, dynamic> ticket) {
    String selectedStatus = ticket['status'] ?? 'open';
    final noteController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Update Status'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            DropdownButtonFormField<String>(
              value: selectedStatus,
              decoration: const InputDecoration(labelText: 'Status'),
              items: const [
                DropdownMenuItem(value: 'open', child: Text('Open')),
                DropdownMenuItem(value: 'in-progress', child: Text('In Progress')),
                DropdownMenuItem(value: 'waiting-parts', child: Text('Waiting Parts')),
                DropdownMenuItem(value: 'completed', child: Text('Completed')),
                DropdownMenuItem(value: 'cancelled', child: Text('Cancelled')),
              ],
              onChanged: (value) {
                selectedStatus = value ?? 'open';
              },
            ),
            TextField(
              controller: noteController,
              decoration: const InputDecoration(labelText: 'Note (optional)'),
              maxLines: 2,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              try {
                await widget.apiService.updateTicketStatus(
                  ticket['id'],
                  selectedStatus,
                  note: noteController.text.isEmpty ? null : noteController.text,
                );
                Navigator.pop(context);
                _loadTickets();
                _showSnackBar('Status updated successfully');
              } catch (e) {
                _showSnackBar('Error updating status: $e');
              }
            },
            child: const Text('Update'),
          ),
        ],
      ),
    );
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}
