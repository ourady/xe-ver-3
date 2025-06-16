import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8'), process.returncode

def check_git_installed():
    output, error, code = run_command("git --version")
    if code != 0:
        print("❌ Git n'est pas installé. Installe-le avant de continuer.")
        sys.exit(1)
    print("✅ Git est installé.")

def check_clean_working_directory():
    output, _, _ = run_command("git status --porcelain")
    if output.strip() != "":
        print("❌ Le répertoire de travail contient des modifications non enregistrées.")
        sys.exit(1)
    print("✅ Le répertoire de travail est propre.")

def switch_to_branch(branch_name):
    _, error, code = run_command(f"git checkout {branch_name}")
    if code != 0:
        print(f"❌ Impossible de passer à la branche '{branch_name}'.\nErreur : {error}")
        sys.exit(1)
    print(f"✅ Branche actuelle : {branch_name}")

def merge_branch(source_branch, target_branch):
    _, error, code = run_command(f"git merge {source_branch}")
    if code != 0:
        print(f"❌ Échec de la fusion de '{source_branch}' dans '{target_branch}'.\nErreur : {error}")
        sys.exit(1)
    print(f"✅ Fusion réussie de '{source_branch}' dans '{target_branch}'.")

def push_changes(branch_name):
    _, error, code = run_command(f"git push origin {branch_name}")
    if code != 0:
        print(f"❌ Échec de l'envoi des modifications sur '{branch_name}'.\nErreur : {error}")
        sys.exit(1)
    print(f"✅ Modifications poussées sur '{branch_name}'.")

def main():
    check_git_installed()
    check_clean_working_directory()
    switch_to_branch("test-quiz")
    merge_branch("main", "test-quiz")
    push_changes("test-quiz")

if __name__ == "__main__":
    main()
