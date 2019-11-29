https://docs.gitlab.com/ee/gitlab-basics/start-using-git.html

Start using Git on the command line
If you want to start using Git and GitLab, make sure that you have created and/or signed into an account on GitLab.

Open a shell
Depending on your operating system, you will need to use a shell of your preference. Here are some suggestions:

Terminal on Mac OSX

GitBash on Windows

Linux Terminal on Linux

Check if Git has already been installed
Git is usually preinstalled on Mac and Linux.

Type the following command and then press enter:

git --version

You should receive a message that tells you which Git version you have on your computer. If you don’t receive a “Git version” message, it means that you need to download Git.

If Git doesn’t automatically download, there’s an option on the website to download manually. Then follow the steps on the installation window.

After you are finished installing Git, open a new shell and type git --version again to verify that it was correctly installed.

Add your Git username and set your email
It is important to configure your Git username and email address, since every Git commit will use this information to identify you as the author.

On your shell, type the following command to add your username:

git config --global user.name "YOUR_USERNAME"

Then verify that you have the correct username:

git config --global user.name

To set your email address, type the following command:

git config --global user.email "your_email_address@example.com"

To verify that you entered your email correctly, type:

git config --global user.email

You’ll need to do this only once, since you are using the --global option. It tells Git to always use this information for anything you do on that system. If you want to override this with a different username or email address for specific projects, you can run the command without the --global option when you’re in that project.

Check your information
To view the information that you entered, along with other global options, type:

git config --global --list

Basic Git commands
Start using Git via the command line with the most basic commands as described below.

Clone a repository
To start working locally on an existing remote repository, clone it with the command git clone <repository path>. By cloning a repository, you’ll download a copy of its files into your local computer, preserving the Git connection with the remote repository.

You can either clone it via HTTPS or SSH. If you chose to clone it via HTTPS, you’ll have to enter your credentials every time you pull and push. With SSH, you enter your credentials once and can pull and push straightaway.

You can find both paths (HTTPS and SSH) by navigating to your project’s landing page and clicking Clone. GitLab will prompt you with both paths, from which you can copy and paste in your command line.

As an example, consider a repository path:

HTTPS: https://gitlab.com/gitlab-org/gitlab-ce.git
SSH: git@gitlab.com:gitlab-org/gitlab-ce.git
To get started, open a terminal window in the directory you wish to clone the repository files into, and run one of the following commands.

Clone via HTTPS:

git clone https://gitlab.com/gitlab-org/gitlab-ce.git

Clone via SSH:

git clone git@gitlab.com:gitlab-org/gitlab-ce.git

Both commands will download a copy of the files in a folder named after the project’s name.

You can then navigate to the directory and start working on it locally.

Go to the master branch to pull the latest changes from there
git checkout master

Download the latest changes in the project
This is for you to work on an up-to-date copy (it is important to do this every time you start working on a project), while you set up tracking branches. You pull from remote repositories to get all the changes made by users since the last time you cloned or pulled the project. Later, you can push your local commits to the remote repositories.

git pull REMOTE NAME-OF-BRANCH

When you first clone a repository, REMOTE is typically “origin”. This is where the repository came from, and it indicates the SSH or HTTPS URL of the repository on the remote server. NAME-OF-BRANCH is usually “master”, but it may be any existing branch.

View your remote repositories
To view your remote repositories, type:

git remote -v

Create a branch
To create a branch, type the following (spaces won’t be recognized in the branch name, so you will need to use a hyphen or underscore):

git checkout -b NAME-OF-BRANCH

Work on an existing branch
To switch to an existing branch, so you can work on it:

git checkout NAME-OF-BRANCH

View the changes you’ve made
It’s important to be aware of what’s happening and the status of your changes. When you add, change, or delete files/folders, Git knows about it. To check the status of your changes:

git status

View differences
To view the differences between your local, unstaged changes and the repository versions that you cloned or pulled, type:

git diff

Add and commit local changes
You’ll see your local changes in red when you type git status. These changes may be new, modified, or deleted files/folders. Use git add to stage a local file/folder for committing. Then use git commit to commit the staged files:

git add FILE OR FOLDER
git commit -m "COMMENT TO DESCRIBE THE INTENTION OF THE COMMIT"

Add all changes to commit
To add and commit all local changes in one command:

git add .
git commit -m "COMMENT TO DESCRIBE THE INTENTION OF THE COMMIT"

Note: The . character typically means all in Git.
Send changes to gitlab.com
To push all local commits to the remote repository:

git push REMOTE NAME-OF-BRANCH

For example, to push your local commits to the master branch of the origin remote:

git push origin master

Delete all changes in the Git repository
To delete all local changes in the repository that have not been added to the staging area, and leave unstaged files/folders, type:

git checkout .

Delete all untracked changes in the Git repository
git clean -f

Unstage all changes that have been added to the staging area
To undo the most recent add, but not committed, files/folders:

git reset .

Undo most recent commit
To undo the most recent commit, type:

git reset HEAD~1

This leaves the files and folders unstaged in your local repository.

Warning: A Git commit is mostly irreversible, particularly if you already pushed it to the remote repository. Although you can undo a commit, the best option is to avoid the situation altogether.
Merge created branch with master branch
You need to be in the created branch.

git checkout NAME-OF-BRANCH
git merge master

Merge master branch with created branch
You need to be in the master branch.

git checkout master

B
B
B
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
B
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
B
B
B
B
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
A
git merge NAME-OF-BRANCH
