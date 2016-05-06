$(function () {

    new Morris.Line({
        element: 'graph_line',
        xkey: 'year',
        ykeys: ['value'],
        labels: ['Value'],
        hideHover: 'auto',
        lineColors: ['#26B99A', '#34495E', '#ACADAC', '#3498DB'],
        data: [
            {year: '2008', value: 20},
            {year: '2009', value: 10},
            {year: '2010', value: 5},
            {year: '2011', value: 5},
            {year: '2012', value: 20}
        ]
    });

});