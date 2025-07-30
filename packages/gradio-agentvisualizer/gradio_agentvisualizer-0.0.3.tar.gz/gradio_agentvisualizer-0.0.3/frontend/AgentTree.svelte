<script lang="ts">
  import AgentTree from './AgentTree.svelte';
  export let value: any;

  const children = value.managed_agents || [];
  const authorized_imports = value.authorized_imports || [];
</script>

<details open style="margin-left: 1em; border: 1px solid #ccc; border-radius: 6px; padding: 0.5em; margin-bottom: 1em;">
  <summary style="font-weight: bold; cursor: pointer;">
    🤖 {value.name}
  </summary>

  <div style="margin-top: 0.5em;">
    <div>✅ <strong>Authorized imports:</strong> {authorized_imports.length > 0 ? authorized_imports.join(', ') : '[]'}</div>
    <div>📝 <strong>Description:</strong> {value.description}</div>

    {#if value.tools && value.tools.length > 0}
      <div style="margin-top: 0.5em;">🛠️ <strong>Tools:</strong></div>
      <table style="width: 100%; border-collapse: collapse; margin-top: 0.5em;">
        <thead>
          <tr>
            <th style="border: 1px solid #ccc; padding: 0.25em;">Name</th>
            <th style="border: 1px solid #ccc; padding: 0.25em;">Description</th>
            <th style="border: 1px solid #ccc; padding: 0.25em;">Arguments</th>
          </tr>
        </thead>
        <tbody>
          {#each value.tools as tool (tool.name)}
            <tr>
              <td style="border: 1px solid #ccc; padding: 0.25em;">{tool.name}</td>
              <td style="border: 1px solid #ccc; padding: 0.25em;">{tool.description}</td>
              <td style="border: 1px solid #ccc; padding: 0.25em;">
                {#each Object.entries(tool.args) as [arg_name, arg]}
                  <div>
                    {arg_name} (<code>{arg.type}</code>): {arg.description}
                  </div>
                {/each}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}

    {#if children.length > 0}
      <div style="margin-top: 0.5em;">└── 🤖 <strong>Managed agents:</strong></div>
      <div style="margin-left: 1em;">
        {#each children as child (child.name)}
          <AgentTree value={child} />
        {/each}
      </div>
    {/if}
  </div>
</details>
