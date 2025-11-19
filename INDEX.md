# 📁 File Index & Navigation Guide

Quick reference for all files in the project and when to use them.

## 🎯 Start Here

| File | Purpose | When to Read |
|------|---------|--------------|
| **[START_HERE.md](START_HERE.md)** | **Complete setup overview** | **First thing to read!** |
| **[README.md](README.md)** | Project overview & quick ref | After START_HERE |
| **[CHECKLIST.md](CHECKLIST.md)** | Step-by-step task list | Throughout the project |

## 📖 Documentation Files

### Setup & Testing
| File | Purpose | When to Use |
|------|---------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Detailed setup guide | Setting up locally |
| [test.py](test.py) | Testing utilities | Testing components |
| [setup.ps1](setup.ps1) | Quick setup script | Initial environment setup |
| [.env.example](.env.example) | Config template | Creating .env file |

### Deployment
| File | Purpose | When to Use |
|------|---------|-------------|
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment instructions | Deploying to cloud |
| [Procfile](Procfile) | Heroku/Render config | Auto-deployment |
| [runtime.txt](runtime.txt) | Python version spec | Platform deployment |

### Submission
| File | Purpose | When to Use |
|------|---------|-------------|
| [SUBMISSION.md](SUBMISSION.md) | Google Form guide | Before submitting form |
| [PROMPTS.md](PROMPTS.md) | Prompt strategies | Writing system/user prompts |

### Understanding
| File | Purpose | When to Use |
|------|---------|-------------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical details | Understanding how it works |
| [WORKFLOW.md](WORKFLOW.md) | Visual diagrams | Visualizing the flow |

## 💻 Core Application Files

### Main Components
| File | Lines | Purpose | Editable |
|------|-------|---------|----------|
| [main.py](main.py) | ~70 | FastAPI server & endpoints | Yes |
| [quiz_solver.py](quiz_solver.py) | ~250 | Quiz solving orchestrator | Yes |
| [browser_handler.py](browser_handler.py) | ~100 | Browser automation | Yes |
| [llm_handler.py](llm_handler.py) | ~150 | OpenAI integration | Yes |
| [data_processor.py](data_processor.py) | ~180 | Data processing | Yes |
| [config.py](config.py) | ~30 | Configuration | Yes |

**Total:** ~780 lines of Python code

## ⚙️ Configuration Files

| File | Purpose | Edit? |
|------|---------|-------|
| [.env.example](.env.example) | Environment template | No - Copy to .env |
| `.env` | Your credentials | **Yes** - Create & edit |
| [.gitignore](.gitignore) | Git ignore rules | Rarely |
| [requirements.txt](requirements.txt) | Python dependencies | Rarely |
| [Procfile](Procfile) | Deployment command | Rarely |
| [runtime.txt](runtime.txt) | Python version | Rarely |

## 📄 Legal & Misc

| File | Purpose |
|------|---------|
| [LICENSE](LICENSE) | MIT License (required) |
| INDEX.md | This file |

## 🗺️ Navigation by Task

### "I want to..."

#### Set up the project
1. Read [START_HERE.md](START_HERE.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Edit `.env` using [.env.example](.env.example)
4. Run `python test.py`

#### Deploy to cloud
1. Read [DEPLOYMENT.md](DEPLOYMENT.md)
2. Choose platform (Render/Railway/etc.)
3. Configure environment variables
4. Deploy and test

#### Submit the form
1. Read [SUBMISSION.md](SUBMISSION.md)
2. Prepare prompts using [PROMPTS.md](PROMPTS.md)
3. Use [CHECKLIST.md](CHECKLIST.md) Phase 7
4. Submit Google Form

#### Understand how it works
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. View [WORKFLOW.md](WORKFLOW.md) diagrams
3. Review core files:
   - [main.py](main.py) - Entry point
   - [quiz_solver.py](quiz_solver.py) - Main logic
   - [browser_handler.py](browser_handler.py) - Browser
   - [llm_handler.py](llm_handler.py) - AI
   - [data_processor.py](data_processor.py) - Data

#### Test the application
1. Run component tests: `python test.py browser`
2. Run LLM test: `python test.py llm`
3. Run full test: `python test.py demo`
4. Check logs for errors

#### Debug issues
1. Check [QUICKSTART.md](QUICKSTART.md) troubleshooting
2. Review error messages
3. Test components individually
4. Check environment variables in `.env`
5. Review relevant core file

#### Prepare for viva
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Understand all core files
3. Review [WORKFLOW.md](WORKFLOW.md) diagrams
4. Practice explaining your choices
5. Use [CHECKLIST.md](CHECKLIST.md) Phase 8

## 📊 File Statistics

### By Type
- **Python code:** 6 files (~780 lines)
- **Documentation:** 9 files (~3000 lines)
- **Configuration:** 5 files
- **Test/Util:** 2 files
- **Legal:** 1 file

### By Purpose
- **Core app:** 6 files (main.py, quiz_solver.py, etc.)
- **Guides:** 9 files (README, QUICKSTART, etc.)
- **Setup:** 5 files (.env, requirements.txt, etc.)
- **Other:** 3 files

**Total:** 23 files

## 🎯 Critical Files (Must Read)

1. **[START_HERE.md](START_HERE.md)** - Complete overview
2. **[QUICKSTART.md](QUICKSTART.md)** - Setup instructions
3. **[SUBMISSION.md](SUBMISSION.md)** - How to submit
4. **[CHECKLIST.md](CHECKLIST.md)** - Task tracker
5. `.env` - Your configuration (create from .env.example)

## 🔧 Files You'll Edit

| File | When | Why |
|------|------|-----|
| `.env` | During setup | Add your credentials |
| [main.py](main.py) | Optional | Customize endpoint behavior |
| [quiz_solver.py](quiz_solver.py) | Optional | Modify solving logic |
| [config.py](config.py) | Optional | Change defaults |

## 📚 Files by Reading Order

### Phase 1: Understanding (30 min)
1. [START_HERE.md](START_HERE.md)
2. [README.md](README.md)
3. [WORKFLOW.md](WORKFLOW.md)

### Phase 2: Setup (1 hour)
1. [QUICKSTART.md](QUICKSTART.md)
2. [.env.example](.env.example)
3. [requirements.txt](requirements.txt)

### Phase 3: Testing (30 min)
1. [test.py](test.py)
2. Error messages
3. [QUICKSTART.md](QUICKSTART.md) troubleshooting

### Phase 4: Deployment (1-2 hours)
1. [DEPLOYMENT.md](DEPLOYMENT.md)
2. [Procfile](Procfile)
3. [runtime.txt](runtime.txt)

### Phase 5: Submission (30 min)
1. [SUBMISSION.md](SUBMISSION.md)
2. [PROMPTS.md](PROMPTS.md)
3. [CHECKLIST.md](CHECKLIST.md)

### Phase 6: Deep Dive (1-2 hours)
1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [main.py](main.py)
3. [quiz_solver.py](quiz_solver.py)
4. [browser_handler.py](browser_handler.py)
5. [llm_handler.py](llm_handler.py)
6. [data_processor.py](data_processor.py)

## 🆘 Quick Troubleshooting Reference

| Problem | Check File | Section |
|---------|-----------|---------|
| Setup issues | QUICKSTART.md | Installation |
| Import errors | requirements.txt | Dependencies |
| Config errors | .env.example | Environment |
| Deployment fails | DEPLOYMENT.md | Platform guide |
| Test failures | test.py | Run tests |
| Code errors | ARCHITECTURE.md | Understanding |
| Submission questions | SUBMISSION.md | Form guide |

## 💡 Tips

- **Bookmark this page** - Useful throughout the project
- **Start with START_HERE.md** - Don't skip it!
- **Use CHECKLIST.md** - Track your progress
- **Read in order** - Documentation builds on itself
- **Test early** - Don't wait to deploy

## 🎓 Learning Path

```
START_HERE.md
    ↓
README.md + WORKFLOW.md
    ↓
QUICKSTART.md → Set up locally
    ↓
test.py → Verify it works
    ↓
DEPLOYMENT.md → Deploy to cloud
    ↓
SUBMISSION.md + PROMPTS.md → Submit form
    ↓
ARCHITECTURE.md → Prepare for viva
    ↓
SUCCESS! 🎉
```

## 📞 Need Help?

1. Check the relevant guide file
2. Review [QUICKSTART.md](QUICKSTART.md) troubleshooting
3. Re-read [START_HERE.md](START_HERE.md)
4. Check logs and error messages
5. Review code comments in core files

---

**Remember:** All documentation is interconnected. Start with [START_HERE.md](START_HERE.md) and follow the links!

*Last updated: November 19, 2025*
