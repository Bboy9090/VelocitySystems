const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

// Import routes
const ticketRoutes = require('./routes/tickets');
const androidRoutes = require('./routes/android');
const iosRoutes = require('./routes/ios');
const firmwareRoutes = require('./routes/firmware');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Make io accessible to routes
app.set('io', io);

// Routes
app.use('/api/tickets', ticketRoutes);
app.use('/api/android', androidRoutes);
app.use('/api/ios', iosRoutes);
app.use('/api/firmware', firmwareRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log('New client connected:', socket.id);

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });

  socket.on('subscribe-ticket', (ticketId) => {
    socket.join(`ticket-${ticketId}`);
    console.log(`Client ${socket.id} subscribed to ticket ${ticketId}`);
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Internal server error',
    message: err.message 
  });
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Socket.IO enabled for real-time updates`);
});

module.exports = { app, io };
