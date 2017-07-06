from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
# set options for play
Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                 'become', 'become_method', 'become_user', 'check'])

#initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='local', module_path='', forks=100, become=True,
                  become_method='sudo', become_user='root', check=False)
passwords = dict(vault_pass='secret')

#create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')
variable_manager.set_inventory(inventory)

#create play with tasks
play_src = dict(
            name="network list",
            hosts="test",
            gather_facts="yes",
            become="true",
            tasks=[
#                dict(name="install basic packages", action="> {{ ansible_pkg_mgr }} name={{ item }} state=present update_cache=yes", with_items="nethogs, iptraf-ng"),
                dict(name="Copy and Execute the script", script="/root/nc.sh", register="result", ignore_errors="yes", args=dict( executable="/bin/bash")),
                dict(name="clear snmp.log",  local_action="shell > /root/snmp.log"),
                dict(name="Show output", action=dict(module="debug", args=dict(msg='{{result.stdout_lines}}'))),
                dict(name="store output", local_action=dict(module="lineinfile", args=dict(line="{{result.stdout_lines}}", dest="/root/snmp.log")))
        ]
       )
play = Play().load(play_src, variable_manager=variable_manager, loader=loader)

#actually run it
tqm = None
try:
    tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback="default",
        )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()

