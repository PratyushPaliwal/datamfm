"#没有定义
[root@ubuntu ～]# ansible-playbook when-1.yaml

PLAY [localhost]
*

TASK [debug]
*

ok: [localhost] => {
"msg": "undefined"
}

PLAY RECAP
*

localhost : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0

#定义
[root@ubuntu ～]# ansible-playbook -e tom=cat when-1.yaml

PLAY [localhost]
*

TASK [debug]
*

skipping: [localhost]

PLAY RECAP
*

localhost : ok=0 changed=0 unreachable=0 failed=0 skipped=1 rescued=0 ignored=0"

范例：循环判断

"[root@ubuntu ~]# cat when-11.yaml\n--- #when-11\n- hosts: localhost\n gather_facts: no\n tasks:\n\t- debug: msg={{ item }}\n\t with_items: [1,2,3,4,5]\n\t when: item > 3"
