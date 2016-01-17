# deterministic-password-generator
Generates passwords from public inputs according to secret user-defined rules

The idea here is to be able to create passwords that have the properties of being:
* Hard to guess
* Hard to brute-force
* Easy to remember
* Unique

Those are conflicting goals, so we adopt schemes like 
[passphrases](https://en.wikipedia.org/wiki/Passphrase) or use passwords
managers.

This project attempts to alleviate the need to entrust a third-party with your
passwords, while still generating passwords that are unique, and easy to
remember.

## Password Derivation

If you just use a normal password and try to remember it, then that password is
your only source of security; that's the thing that it's your responsibility to
remember, and it's effectively the keys to whatever you protect with it.

If you use a password manager, then you have a single password that's the key
to all your other passwords - that is, given that password, all your others can
be found. Here, your security comes from the fact that only you know the master
password.

The idea of deterministic-password-generator is to augment your master-password
with a different sort of master-key; here, your security comes from the fact
that you're the only one who knows the system of rules by which your passwords
can be generated (while the ingredients to do so, _given_ those rules, might be
public, or easy to guess).

We call the inputs (that will change based on which service you're logging in
to, for example, or your username) the "password `seed`s", while the rules that
determine how your password is derived from those seeds are the `ruleset`

## Setup

You'll need to define a ruleset - this is a piece of python code that, given
a set of inputs, generated your password.

Your ruleset is your private secret here - don't check it in to git, or store
it in an insecure location. Treat it like you would a private ssh key.

_Ideally_, your ruleset is really just an _extra_ piece of secret information;
there's no reason you shouldn't _always_ use some sort of (secret) master
password as one of your seeds.

### Your rules

Your rules take the form of a python module. The only requirements are:
* Your rules are in a folder which can be imported as a valid python module
* Your rules expose a method: `generate_password` which accepts a list of 
`parts` and returns a generated password

Compile your rules into a `ruleset` by doing:
```sh
~: dpg compile /path/to/your/super_secret_scheme
~: ls
super_secret_scheme.dpgr
```

You will be asked for a password that will be used to encrypt your ruleset
once it's compiled into a ruleset package.

Once they're compiled, install your rules into your rule repository:
```sh
~: dpg install_ruleset super_secret_schema.dpgr
```

## Usage

```sh
~: dpg generate_password <ruleset_name> password parts derived from easy to to remember knowledge
```

Again, you'll be asked for a password that will decrypt your ruleset.

e.g.

```sh
~: dpg generate_password super_secret_schema jelford @ github super_secret_password
hf<jfJfdpane#,f1
```

## Example

If you check out the source, you can see two basic example rulesets in the 
`tests` folder:
* `mock_ruleset_simple`
* `mock_ruleset_multifile`

You can do:
```sh
~: dpg compile_ruleset ./tests/mock_ruleset_simple
Password (used to encrypt compiled ruleset): ...
~: dpg install_ruleset ./mock_ruleset_simple.dpgr
~: dpg generate_password jelford @ github.com
Password (to decrypt ruleset): ...
> jelford@github.com
```