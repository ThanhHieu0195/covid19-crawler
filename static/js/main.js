
function affectData(details) {
    if (details) {
        let arr = []
        let idx = 1;
        for (const r of details) {
            arr.push('<td>' + [
                `<span class="lb">${idx}</span>`,
                `<span class="lb-info">${r.region}</span>`,
                `<span class="lb-text">${formatNumber(r.case_numbers)}</span>`,
                `<span class="lb-warn">${formatNumber(r.today)}</span>`,
                `<span class="lb-danger">${formatNumber(r.dead)}</span>`,
            ].join('</td><td>') + '</td>');
            idx ++;
        }

        $('.js-detail').html('<tr><th>' + [
            '', 'Khu vực', 'Tổng ca nhiễm', 'Hôm nay', 'Tổng số người chết'
        ].join('</th><th>') + '</th></tr>' + '<tr>' + arr.join('</tr><tr>') + '</tr>');
    }
}

function formatNumber(num) {
    return num.toFixed(1).replace(/\d(?=(\d{3})+\.)/g, '$&,').replace('.0', '')
}

(async function ($) {
    previousData = null;
    const fetchData = async function () {
        const d = await $.get('/covid19');
        d.details = d.details.sort((a, b) => b.today - a.today)
        console.log('start fetch data')
        if (!previousData || previousData.case_numbers != d.case_numbers) {
            if (previousData) {
                $.notify("New update", "success");
            }
            affectData(d.details)
            $('.js-numbercase').html(formatNumber(d.case_numbers))
            $('.js-increase').html(formatNumber(d.increase))

            let t = '' + d.last_updated
            let seconds = /\d{2}$/.exec(t)[0]
            $('.js-time').html(`cập nhật lúc: ${t.replace(seconds, '')}:${seconds}`)
        }
        previousData = d;
    }

    await fetchData();
    setInterval(async function () {
        await fetchData()
    }, 5000);

    $('.js-search').on('keyup', function (e) {
        let v = $('.js-search').val().trim()
        if (v) {
            affectData(previousData.details.filter(i => i.region.toLowerCase().match(v.toLowerCase())))
        } else {
            affectData(previousData.details)
        }
    });

    const today = new Date()
    $('.js-today').html(`${today.toISOString().replace(/T(.*)/, '')}`)
})(jQuery);