
async function calcAll()
{
    var locationA = document.getElementById("locationA").value;
    var locationB = document.getElementById("locationB").value;
    console.log("locationA",locationA)
    console.log("locationB",locationB)

    var ab_url = "/api/v1.0/covid_data_ab/locationA/locationB";
    ab_url = ab_url.replace("locationA", locationA);
    ab_url = ab_url.replace("locationB", locationB);

    var ab_data = await d3.json(ab_url);
    genTable(ab_data)
    

    var predict_url = "/api/v1.0/predict_fully_vaccinated/location";
    a_predict_url = predict_url.replace("location", locationA);
    b_predict_url = predict_url.replace("location", locationB);
    var a_prediction_data = await d3.json(a_predict_url);
    var b_prediction_data = await d3.json(b_predict_url);

    genChart(ab_data, a_prediction_data, b_prediction_data, locationA, locationB)
    
}

function genTable(data)
{
  d3.select('tbody').html('');
        data.forEach(obj => {
            var row = d3.select('tbody').append('tr');
            Object.values(obj).forEach(val => {
                row.append('td').text(val)
            })
        });
}


function genChart(data, a_prediction_data, b_prediction_data, locationA, locationB)
{
    let A_data = data.filter(day => day.find(element => element == locationA));
    let B_data = data.filter(day => day.find(element => element == locationB));

    let A_dates = A_data.map(day => day[0]);
    let B_dates = B_data.map(day => day[0]);

    let A_people = A_data.map(day => day[7]);
    let B_people = B_data.map(day => day[7]);

    let prediction_A_dates = a_prediction_data.map(day => day[0]);
    let prediction_B_dates = b_prediction_data.map(day => day[0]);
    let prediction_A_people = a_prediction_data.map(day => day[1]);
    let prediction_B_people = b_prediction_data.map(day => day[1]);
    

    var trace1 =
    {
        x: A_dates,
        y: A_people,
        type: 'scatter',
        name: locationA,
        line: {
            width: 3
        }
    };

    var trace2 =
    {
        x: B_dates,
        y: B_people,
        type: 'scatter',
        name: locationB,
        line: {
            width: 3
        }
    };

    var trace3 =
    {
        x: prediction_A_dates,
        y: prediction_A_people,
        type: 'scatter',
        name: locationA+" prediction",
        line: {
            dash: 'dot',
            width: 2
        }
    };

    var trace4 =
    {
        x: prediction_B_dates,
        y: prediction_B_people,
        type: 'scatter',
        name: locationB+" prediction",
        line: {
            dash: 'dot',
            width: 2
        }
    };

    var layout = {
        title:'Dates VS People Vacinates per 100',
        yaxis: {range: [0, 100]}
    };

    var data = [trace1, trace3, trace2, trace4];

    Plotly.newPlot('covid_data_line_chart', data, layout);
}
