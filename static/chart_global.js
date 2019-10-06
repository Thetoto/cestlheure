const next_date = {
    year: new Date().getFullYear(),
    month: new Date().getMonth() + 1
}
const data_colors = ["rgb(255, 99, 132)", "rgb(75, 192, 192)", "rgb(201, 203, 207)", "rgb(255, 159, 64)", "rgb(153, 102, 255)", "rgb(255, 99, 132)", "rgb(255, 205, 86)","rgb(255, 99, 132)", "rgb(75, 192, 192)", "rgb(201, 203, 207)", "rgb(255, 159, 64)", "rgb(153, 102, 255)", "rgb(255, 99, 132)", "rgb(255, 205, 86)"];

function compare_date(date1, date2) {
    if (date1.year > date2.year)
        return 1
    if (date1.year == date2.year) {
        if (date1.month > date2.month)
            return 1;
        if (date1.month == date2.month)
            return 0; // (equality)
    }
    return -1; // (date 2 greater)
}

function add_one_date(date) {
    date.month += 1;
    if (date.month >= 13) {
        date.month = 1;
        date.year += 1;
    }
    return date;
}

let chart_dataset = [];
for (let i in chart_bymonth) {
    let date = {
        year: 2018,
        month: 12
    };
    let datas = [];
    let index = 0;
    console.log("here");
    while (compare_date(next_date, date) != -1) {
        console.log(chart_bymonth[i].date[index]);
        console.log(chart_bymonth[i].count[index]);
        if (chart_bymonth[i].date[index] && compare_date(date, chart_bymonth[i].date[index]) == 0) {
            datas.push(chart_bymonth[i].count[index]);
            index++;
        } else {
            datas.push(null);
        }
        date = add_one_date(date);
    }
    chart_dataset.push({
        label: chart_bymonth[i].sender[0].name,
        fill: false,
        backgroundColor: data_colors[i],
        borderColor: data_colors[i],
        data: datas,
    });
}
let labels = [];
let date = {
    year: 2018,
    month: 12
};
while (compare_date(next_date, date) != -1) {
    labels.push(date.month + "/" + date.year);
    date = add_one_date(date);
}
console.log(chart_dataset);
var config = {
    type: 'line',
    data: {
        labels: labels,
        datasets: chart_dataset
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        title: {
            display: true,
            text: 'Classement par mois'
        },
        tooltips: {
            mode: 'nearest',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: false
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Mois'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Points'
                }
            }]
        }
    }
};

window.onload = function () {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};