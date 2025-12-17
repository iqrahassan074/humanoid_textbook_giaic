# Physical AI Textbook Frontend

This is the frontend for the Physical AI Textbook platform, built with Docusaurus. It provides a textbook reading experience with an integrated AI assistant that can answer questions about the content.

## Features

- **Textbook Chapters**: 6 comprehensive chapters on Physical AI
- **AI Assistant**: Chatbot that answers questions with citations to source material
- **User Authentication**: Login and registration system
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, accessible interface

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Configuration

The frontend connects to the backend API at `http://localhost:8000/api/v1` by default. To change this:

1. Create a `.env` file in the frontend directory:
```bash
REACT_APP_API_URL=http://your-backend-url:port
```

## Running the Development Server

```bash
npm start
```

This will start the development server at `http://localhost:3000`.

## Building for Production

```bash
npm run build
```

This creates a `build` directory with the optimized production build.

## Project Structure

```
frontend/
├── docs/                 # Textbook chapters
│   └── chapters/         # Individual chapter files
├── src/
│   ├── components/       # React components
│   │   └── ChatbotWidget.js
│   ├── contexts/         # React contexts
│   │   └── AuthContext.js
│   ├── pages/            # Special pages
│   │   ├── login.js
│   │   ├── register.js
│   │   └── chatbot.js
│   ├── services/         # API services
│   │   └── chatbotAPI.js
│   ├── css/              # Custom styles
│   │   └── custom.css
│   └── theme/            # Docusaurus theme overrides
│       ├── Root.js
│       └── Doc.js
├── static/               # Static assets
├── src/                  # Docusaurus source
├── docusaurus.config.js  # Docusaurus configuration
├── sidebars.js          # Navigation sidebars
└── package.json         # Dependencies and scripts
```

## Key Components

### ChatbotWidget
- Floating chatbot widget available on all pages
- Allows asking questions about textbook content
- Displays answers with citations and confidence scores

### AuthContext
- Manages user authentication state
- Handles login, registration, and logout
- Stores authentication tokens

### ChatbotAPI
- Service layer for communicating with backend
- Handles question submission and response retrieval
- Manages authentication headers

## Backend Integration

The frontend communicates with the backend API at these endpoints:

- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/chatbot/ask` - Ask a question to the AI assistant
- `GET /api/v1/chatbot/history` - Get question history

## Customization

### Adding New Chapters
1. Create a new markdown file in `docs/chapters/`
2. Follow the format of existing chapters
3. Update `sidebars.js` to include the new chapter

### Styling
- Custom styles are in `src/css/custom.css`
- Docusaurus uses Infima CSS framework
- Override theme components in `src/theme/`

## Deployment

The site can be deployed to various platforms:

### GitHub Pages
```bash
npm run deploy
```

### Other Platforms
- Netlify, Vercel, AWS S3, etc.
- Build the site with `npm run build`
- Serve the `build` directory

## Troubleshooting

### API Connection Issues
- Ensure the backend server is running at the configured URL
- Check browser console for CORS errors
- Verify authentication tokens are properly stored

### Chatbot Not Working
- Confirm Claude API key is configured in backend
- Check that the RAG pipeline is properly set up
- Verify vector database (Qdrant) is running

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[License information goes here]