const DATA_COUNT = 7;
const NUMBER_CFG = {count: DATA_COUNT, min: -100, max: 100};

const renderDealsPerMonth = async () => {
    const res = await fetch("http://localhost:5001/dealsPerMonth");
    const data = await res.json();

    new Chart(
        document.querySelector("#dealsPerMonthChart"),
        {
          type: 'pie',
          data: {
              labels: data.map(e => e.month),
              datasets: [
                {
                  label: 'Fully Rounded',
                  data: data.map(e => e.deals),
                  borderWidth: 2,
                  borderRadius: Number.MAX_VALUE,
                  borderSkipped: false,
                }
              ]
            },
          options: {
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Chart.js Bar Chart'
              }
            }
          },
        }
    );
}

renderDealsPerMonth();

const renderValuePerCompany = async () => {
    const res = await fetch("http://localhost:5001/valuePerCompany");
    const data = await res.json();

    new Chart(
        document.querySelector("#valuePerCompanyChart"),
        {
          type: 'pie',
          data: {
              labels: data.map(d => d.company_name),
              datasets: [
                {
                  label: 'Fully Rounded',
                  data: data.map(d => d.value),
                  borderWidth: 2,
                  borderRadius: Number.MAX_VALUE,
                  borderSkipped: false,
                }
              ]
            },
          options: {
            plugins: {
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Chart.js Bar Chart'
              }
            }
          }
        }
    );
}

renderValuePerCompany();
