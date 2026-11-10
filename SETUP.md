# Trainee GitHub setup guide

Finish this before the week 1 seminar. It takes 30–45 minutes. Every step is required.

You will use **your own personal GitHub account** for the whole course. Do not use a shared, borrowed or
institutional account. Your pull requests, transcripts and journal become your portfolio, so the account must be yours.

## 1. Create your account

1. Go to github.com and sign up with an email address you will still have after you graduate.
2. Choose a professional username: you will put it on your CV. `firstname-lastname` or similar works.
3. Verify your email address.
4. Add your real name and a photo or avatar under **Settings → Public profile**.

## 2. Turn on two-factor authentication (2FA)

1. **Settings → Password and authentication → Enable two-factor authentication.**
2. Use an authenticator app (or a passkey or security key). Avoid SMS if you can.
3. **Download your recovery codes and store them somewhere safe and offline.** Losing your phone without them can lock you out for good.

The course organisation requires 2FA. You cannot join without it.

## 3. Add an SSH key

On your own laptop:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
# press Enter to accept the default path; set a passphrase
cat ~/.ssh/id_ed25519.pub
```

Copy the line that starts with `ssh-ed25519`, then **Settings → SSH and GPG keys → New SSH key**, paste and save.
Test it:

```bash
ssh -T git@github.com
# "Hi <username>! You've successfully authenticated..."
```

## 4. Configure Git

```bash
git config --global user.name  "Your Name"
git config --global user.email "the-email-on-your-github-account"
git config --global init.defaultBranch main
```

## 5. Join the course organisation

1. Post your GitHub username to the instructor as asked at enrolment.
2. Accept the invitation email (or visit `github.com/the course organisation`) and accept.
3. In `course-tracker`, find the issue with your name and comment: `Ready: @your-username`.

## 6. Install the tools

- Git, a code editor, Python 3.11+, Docker (or use GitHub Codespaces from week 9).
- The GitHub CLI: `gh auth login`.
- The course harness and local model as described in the course manual's toolchain section.

## 7. Check yourself

- [ ] I can sign in with 2FA and I have my recovery codes saved
- [ ] `ssh -T git@github.com` greets me by name
- [ ] I am a member of the course organisation
- [ ] I commented `Ready` on my tracker issue

## Rules for the course

- **Never commit secrets.** API keys go in environment variables or GitHub Actions secrets, never in code, `AGENTS.md` or issues.
- **Every submission is a pull request** with the PR template filled in: transcript link, autonomy level, token budget.
- **Your fork, your account.** Do not push to someone else's repository unless you are on their team.
