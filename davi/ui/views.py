from django.shortcuts import render
from django.http import HttpResponse

from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret

import io

from davi.ui.forms import VaultForm


def main(request):
    if request.method == 'POST':
        form_posted = VaultForm(request.POST)
        if form_posted.is_valid():
            vault = VaultLib([(
                DEFAULT_VAULT_ID_MATCH,
                VaultSecret(form_posted.cleaned_data['password'].encode()))])

            if form_posted.cleaned_data['yaml'] and not form_posted.cleaned_data['vault']:
                vault = vault.encrypt(form_posted.cleaned_data['yaml']).decode()
                form = VaultForm(
                    initial={
                        'password': form_posted.cleaned_data['password'],
                        'yaml': form_posted.cleaned_data['yaml'],
                        'vault': vault})

                action = 'chiffrement'

            elif form_posted.cleaned_data['vault'] and not form_posted.cleaned_data['yaml']:
                vault_stringio = io.StringIO(form_posted.cleaned_data['vault'])
                yaml =  vault.decrypt(vault_stringio.read()).decode()
                form = VaultForm(
                    initial={
                        'password': form_posted.cleaned_data['password'],
                        'yaml': yaml,
                        'vault': form_posted.cleaned_data['vault']})

                action = 'déchiffrement'

            else:
                form = VaultForm(
                    initial={
                        'password': form_posted.cleaned_data['password'],
                        'yaml': form_posted.cleaned_data['yaml'],
                        'vault': form_posted.cleaned_data['vault']})

                action = 'vous attendez quoi ?'

    else:
        action = ''
        form = VaultForm()

    return render(request, 'main.html', {'form': form, 'action': action})
