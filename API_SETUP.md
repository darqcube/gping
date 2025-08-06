# Globalping API Setup Instructions

## Step 1: Get Your Globalping API Key

### 1. Visit the Globalping Website
- Go to [https://globalping.io](https://globalping.io)
- Click on "Sign Up" or "Get Started" in the top navigation

### 2. Create an Account
- Fill in your email address
- Choose a password
- Complete the registration process
- Verify your email address if required

### 3. Access Your API Key
- After logging in, go to your **Dashboard** or **Account Settings**
- Look for a section called **"API Keys"** or **"Developer Settings"**
- Click on **"Generate API Key"** or **"Create New Key"**
- Give your API key a descriptive name (e.g., "Traceroute Visualizer")
- Copy the generated API key (it will look something like: `glp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 4. API Key Format
Your API key should look like this:
```
glp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 2: Create the .env File

### 1. Create .env file in your project root
Create a new file called `.env` in the same directory as your `globalping_traceroute.py` file.

### 2. Add your API key to the .env file
Open the `.env` file and add your API key:

```env
GLOBALPING_API_TOKEN=glp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Replace `glp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual API key.**

### 3. Example .env file content:
```env
# Globalping API Configuration
GLOBALPING_API_TOKEN=glp_your_actual_api_key_here

# Optional: Flask Environment
FLASK_ENV=development
```

## Step 3: Verify Setup

### 1. Test the API Key
You can test if your API key works by running a simple test:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.globalping.io/v1/probes
```

Replace `YOUR_API_KEY` with your actual API key.

### 2. Run the Application
- Start your Docker container: `docker-compose up --build`
- Or run locally: `python globalping_traceroute.py`
- Visit `http://localhost:5001`
- Try performing a traceroute to test if the API key is working

## Step 4: Docker Environment Variables (Optional)

If you're using Docker and want to set the API key as an environment variable instead of using the .env file:

### Option A: Docker Compose
Add to your `docker-compose.yml`:

```yaml
services:
  globalping-traceroute:
    # ... other configuration
    environment:
      - GLOBALPING_API_TOKEN=glp_your_actual_api_key_here
      - FLASK_ENV=production
```

### Option B: Docker Run Command
```bash
docker run -d -p 5001:5001 \
  -e GLOBALPING_API_TOKEN=glp_your_actual_api_key_here \
  --name globalping-app globalping-traceroute
```

## Troubleshooting

### API Key Not Working?
1. **Check the format**: Make sure your API key starts with `glp_`
2. **Verify the key**: Test with curl command above
3. **Check permissions**: Ensure your account has API access
4. **Rate limits**: Free accounts may have rate limits

### Common Issues:
- **"Invalid API key"**: Double-check the key format and copy/paste
- **"Rate limit exceeded"**: Wait a few minutes or upgrade your plan
- **"Unauthorized"**: Make sure your account is verified

### Getting Help:
- Visit [Globalping Documentation](https://docs.globalping.io)
- Check [Globalping Community](https://community.globalping.io)
- Contact Globalping support if needed

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit your .env file to version control**
   - Add `.env` to your `.gitignore` file
   - The `.env` file is already in `.dockerignore`

2. **Keep your API key private**
   - Don't share it in public repositories
   - Don't include it in screenshots or logs

3. **Rotate your API key if compromised**
   - Generate a new key in your Globalping dashboard
   - Update your .env file with the new key

## File Structure After Setup

Your project should look like this:
```
gping/
├── globalping_traceroute.py
├── templates/
│   └── index.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                    ← Your API key goes here
├── .gitignore             ← Should include .env
└── API_SETUP.md          ← This file
```

## Next Steps

After setting up your API key:
1. Test the application with a simple traceroute
2. Explore the filtering features
3. Customize the visualization as needed
4. Deploy to your preferred hosting platform 