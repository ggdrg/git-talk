import re
import git_talk.lib.gfunc as gfunc
import git_talk.lib.cutie as cutie

import git_talk.menu.status as stts
def gitflow(cc, repo):
    '''
    create gitflow structure
    master=prod,release=release,dev=dev,hotfix=hotfix,feature=feature 
    '''
    #
    # git config --global alias.hist "log --graph --date-order --date=short --pretty=format:'%C(auto)%h%d %C(reset)%s %C(bold blue)%ce %C(reset)%C(green)%cr (%cd)'"

    #Usage:
    # git hist - Show the history of current branch
    # git hist --all - Show the graph of all branches (including remotes)
    # git hist master devel - Show the relationship between two or more branches
    # git hist --branches - Show all local branches

    # Add --topo-order to sort commits topologically, instead of by date (default in this alias)

    # Benefits:
    # Looks just like plain --decorate, so with separate colors for different branch names
    # Adds committer email
    # Adds commit relative and absolute date
    # Sorts commits by date
    # Setup:
    
    cmd = [["git", "hist", "--branches"]]

    b, error = gfunc.subprocess_cmd(repo['path'], cmd)
    # print(b)

def git_graph(cc, repo, time):
    # [alias]
    # good one lg1 = git log --since="4 hours ago" --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
    # lg2 = git log --since="4 hours ago" --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' --all
    # lg = !"git lg1"
    pass

def git_simple(cc, repo):
    count = 0
    current_branch, remote_status = stts.current_status(cc, repo)
    c=[['git', 'checkout', 'master']]
    result = gfunc.subprocess_cmd(repo["path"], c)

    c=[['git', 'log', '--graph', '--oneline', '--decorate', '-2000']]
    result,error = gfunc.subprocess_cmd(repo["path"], c, display=False)
    if error != 0:
        cutie.cprint('error',result[0])
        return 
        
    cutie.color_print('WHITE','\n----------------------- Git Graph (last 20 branch level event)-----------------------')
    for r in result[0].split('\n'):
        if count > 20:
            break
        if '*' in r:
            if 'Merge pull request' in r: 
                cutie.color_print('GREEN',string_filter(r))
                count += 1            
            elif '(' in r :
                cutie.color_print('YELLOW', string_filter(r))
                count += 1
            else:
                pass
                # cutie.color_print('MAGENTA', string_filter(r))
                # count += 1                
        else:
            cutie.color_print('WHITE',r)
            count += 1
    cutie.color_print('WHITE','\n----------------------- Git Graph             (end)          -----------------------\n')
    c=[['git','checkout', current_branch]]
    result,error = gfunc.subprocess_cmd(repo["path"], c)

def string_filter(r):
    f = r'origin/\S*(, |\))'
    r = re.sub(f,'', r)
    return r