const express = require('express');
const router = express.Router();
const { v4: uuidv4 } = require('uuid');

// In-memory storage (replace with database in production)
let tickets = [];

// Get all tickets
router.get('/', (req, res) => {
  try {
    const { status, customerId } = req.query;
    let filteredTickets = tickets;

    if (status) {
      filteredTickets = filteredTickets.filter(t => t.status === status);
    }
    if (customerId) {
      filteredTickets = filteredTickets.filter(t => t.customer.id === customerId);
    }

    res.json({
      success: true,
      count: filteredTickets.length,
      tickets: filteredTickets
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Get single ticket
router.get('/:id', (req, res) => {
  try {
    const ticket = tickets.find(t => t.id === req.params.id);
    if (!ticket) {
      return res.status(404).json({ success: false, error: 'Ticket not found' });
    }
    res.json({ success: true, ticket });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Create new ticket
router.post('/', (req, res) => {
  try {
    const { customer, device, issue, priority } = req.body;

    if (!customer || !device || !issue) {
      return res.status(400).json({ 
        success: false, 
        error: 'Missing required fields: customer, device, issue' 
      });
    }

    const newTicket = {
      id: uuidv4(),
      ticketNumber: `TKT-${Date.now()}`,
      customer: {
        id: customer.id || uuidv4(),
        name: customer.name,
        email: customer.email,
        phone: customer.phone
      },
      device: {
        type: device.type, // 'android' or 'ios'
        manufacturer: device.manufacturer,
        model: device.model,
        serialNumber: device.serialNumber,
        imei: device.imei
      },
      issue: {
        description: issue.description,
        category: issue.category,
        severity: issue.severity || 'medium'
      },
      status: 'open',
      priority: priority || 'normal',
      estimatedCost: 0,
      actualCost: 0,
      diagnostics: {},
      repairHistory: [],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    tickets.push(newTicket);

    // Emit socket event for new ticket
    const io = req.app.get('io');
    io.emit('ticket-created', newTicket);

    res.status(201).json({ success: true, ticket: newTicket });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Update ticket
router.put('/:id', (req, res) => {
  try {
    const ticketIndex = tickets.findIndex(t => t.id === req.params.id);
    if (ticketIndex === -1) {
      return res.status(404).json({ success: false, error: 'Ticket not found' });
    }

    const updatedTicket = {
      ...tickets[ticketIndex],
      ...req.body,
      updatedAt: new Date().toISOString()
    };

    tickets[ticketIndex] = updatedTicket;

    // Emit socket event for ticket update
    const io = req.app.get('io');
    io.to(`ticket-${req.params.id}`).emit('ticket-updated', updatedTicket);

    res.json({ success: true, ticket: updatedTicket });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Update ticket status
router.patch('/:id/status', (req, res) => {
  try {
    const { status, note } = req.body;
    const ticketIndex = tickets.findIndex(t => t.id === req.params.id);
    
    if (ticketIndex === -1) {
      return res.status(404).json({ success: false, error: 'Ticket not found' });
    }

    const validStatuses = ['open', 'in-progress', 'waiting-parts', 'completed', 'cancelled'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ 
        success: false, 
        error: `Invalid status. Valid statuses: ${validStatuses.join(', ')}` 
      });
    }

    tickets[ticketIndex].status = status;
    tickets[ticketIndex].updatedAt = new Date().toISOString();
    
    const historyEntry = {
      timestamp: new Date().toISOString(),
      action: 'status-change',
      previousStatus: tickets[ticketIndex].status,
      newStatus: status,
      note: note || ''
    };
    
    tickets[ticketIndex].repairHistory.push(historyEntry);

    // Emit socket event
    const io = req.app.get('io');
    io.to(`ticket-${req.params.id}`).emit('ticket-status-changed', {
      ticketId: req.params.id,
      status,
      note
    });

    res.json({ success: true, ticket: tickets[ticketIndex] });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Add diagnostic data to ticket
router.post('/:id/diagnostics', (req, res) => {
  try {
    const ticketIndex = tickets.findIndex(t => t.id === req.params.id);
    if (ticketIndex === -1) {
      return res.status(404).json({ success: false, error: 'Ticket not found' });
    }

    tickets[ticketIndex].diagnostics = {
      ...tickets[ticketIndex].diagnostics,
      ...req.body,
      timestamp: new Date().toISOString()
    };
    tickets[ticketIndex].updatedAt = new Date().toISOString();

    // Emit socket event
    const io = req.app.get('io');
    io.to(`ticket-${req.params.id}`).emit('diagnostics-updated', {
      ticketId: req.params.id,
      diagnostics: tickets[ticketIndex].diagnostics
    });

    res.json({ success: true, ticket: tickets[ticketIndex] });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// Delete ticket
router.delete('/:id', (req, res) => {
  try {
    const ticketIndex = tickets.findIndex(t => t.id === req.params.id);
    if (ticketIndex === -1) {
      return res.status(404).json({ success: false, error: 'Ticket not found' });
    }

    const deletedTicket = tickets.splice(ticketIndex, 1)[0];

    // Emit socket event
    const io = req.app.get('io');
    io.emit('ticket-deleted', { ticketId: req.params.id });

    res.json({ success: true, ticket: deletedTicket });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;
