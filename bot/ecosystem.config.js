module.exports = {
  apps: [
    {
      name: 'MindfulInspiroBot',
      script: './main.py',
      watch: true,
      log_date_format: 'YYYY-MM-DD HH Z',
      error_file: './logs/MIB/error.log',
      out_file: './logs/MIB/out.log',
      max_size: '10M', // Example: Rotate the log after it reaches 10 Megabytes
      combine_logs: true, // Combine log files across all instances of the app
      time: true
    }
  ],

  deploy: {
    production: {
      'pre-deploy-local': '',
      'post-deploy':
        'pip install -r requirements.txt && pm2 reload ecosystem.config.js',
      'pre-setup': ''
    }
  }
};
