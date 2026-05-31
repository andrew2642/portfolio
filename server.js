const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Contact Endpoint
app.post('/contact', async (req, res) => {
    const { user_name, user_email, message } = req.body;
    console.log(`[RECV] Incoming transmission from: ${user_name} (${user_email})`);

    if (!user_name || !user_email || !message) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    // Create a transporter using SMTP
    // IMPORTANT: Use environment variables for your actual credentials!
    const transporter = nodemailer.createTransport({
        service: 'gmail',
        auth: {
            user: process.env.EMAIL_USER,
            pass: process.env.EMAIL_PASS, // Use an App Password for Gmail
        },
    });

    const mailOptions = {
        from: user_email,
        to: process.env.RECEIVER_EMAIL || process.env.EMAIL_USER,
        subject: `New Portfolio Mission: ${user_name}`,
        text: `Commander Andrew,\n\nYou have received a new mission briefing:\n\nName: ${user_name}\nEmail: ${user_email}\n\nMessage:\n${message}`,
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log(`[SUCCESS] Email sent to ${mailOptions.to}`);
        res.status(200).json({ message: 'Transmission received successfully!' });
    } catch (error) {
        console.error('[CRITICAL] SMTP Error:', error.message);
        res.status(500).json({ error: 'Failed to send transmission.' });
    }
});

app.listen(PORT, () => {
    console.log(`Command Center operational on port ${PORT}`);
});