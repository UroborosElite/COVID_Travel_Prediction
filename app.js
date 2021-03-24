
d3.csv('full_df.csv').then(data => {

    showData(data);

    function showData(data) {
        d3.select('tbody').html('');
        data.forEach(obj => {
            var row = d3.select('tbody').append('tr');
            Object.values(obj).forEach(val => {
                row.append('td').text(val)
            })
        });
    };


    d3.selectAll('input').on('change', handleChange);

    var filteredData = data;

    function handleChange() {
        var id = d3.select(this).property('id');
        var value = d3.select(this).property('value');

        filteredData = filteredData.filter(obj => obj[id] == value)

        showData(filteredData)
    }

    d3.select('button').on('click',handleClick);
    
    function handleClick() {
        filteredData = data;
        showData(filteredData);
    }
});

