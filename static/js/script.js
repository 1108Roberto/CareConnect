document.addEventListener("DOMContentLoaded", () => {
  const clientId = document.getElementById("client-details")?.dataset.clientId;

  if (clientId && clientId !== "all") {
    loadClientDetails(clientId);
    loadClientPolicies(clientId);
    loadClientClaims(clientId);
  } else {
    loadAllClients();
  }
});

async function loadClientDetails(clientId) {
  try {
    const response = await fetch(`/api/clients/${clientId}/`);
    const data = await response.json();

    document.getElementById("client-name").textContent = data.name;
    document.getElementById("client-id").textContent = data.national_id;
    document.getElementById("client-address").textContent = data.address;
    document.getElementById("client-phone").textContent = data.phone;
    document.getElementById("client-email").textContent = data.email;
  } catch (error) {
    console.error("Error loading client details:", error);
  }
}

async function loadClientPolicies(clientId) {
  try {
    const response = await fetch(`/api/clients/${clientId}/policies/`);
    const policies = await response.json();

    const tbody = document.querySelector("#policies-table tbody");
    tbody.innerHTML = policies
      .map(
        (policy) => `
            <tr>
                <td>${policy.policy_number}</td>
                <td>${policy.branch}</td>
                <td class="status-${policy.status.toLowerCase()}">${
          policy.status
        }</td>
                <td>${new Date(policy.end_date).toLocaleDateString()}</td>
                <td>
                    <button class="view-policy" data-policy-id="${
                      policy.policy_id
                    }">View</button>
                </td>
            </tr>
        `
      )
      .join("");
  } catch (error) {
    console.error("Error loading policies:", error);
  }
}

// NOTE: Add similar functions for claims and event listeners
