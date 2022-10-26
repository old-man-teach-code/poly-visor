<script>
    import {system} from "../store/supstore";
    import {processes} from "../store/supstore";
    import {count} from "../store/supstore";
    import {chartJS} from "../store/action.js";

    let data = {
        type: 'line',
			data: {
					labels: ["60s","55s","50s","45s","40s","35s","30s","25s","20s","15s","10s","5s","0s"],
					datasets: [{
                        label: 'CPU %',
						backgroundColor: "#FF8C32",
						borderColor: 'rgb(255, 99, 132)',
						data:  Array(13)
						}]
				    },
            options: {
            fill:true,
            responsive: true,
            plugins: {
                legend: {
                    position: "top"
                },
                title: {
                    display: true,
                    text: "Overall CPU usage"
                }
            },
            scales: {
            y: {
                suggestedMin: 0,
                suggestedMax: 50
            }
        }
        }        
    };

    setInterval(() => {
        data.data.datasets.forEach((ds) => {
            ds.data.shift();
            ds.data.push($system.cpu);
    });
        data = data;
    }, 1000);

        </script>
<div class="w-full px-10">
    <h1 class=" pt-5 text-2xl font-semibold">Overview</h1>
        <div class="grid text-center justify-items-center items-end gap-5 grid-cols-4 grid-rows-4">
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">CPU Usage</h1><h4>{$system.cpu}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Ram Usage</h1><h4>{$system.memory}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Running process</h1><h4>{$count}</h4></div>
            <div class="border-2 bg-white w-full h-32 rounded-xl"><h1 class="text-xl pt-4">Total process</h1><h4>{Object.keys($processes).length}</h4></div>
            <div class="border-2 bg-white w-full h-full rounded-xl row-span-3 col-span-4" >
                <canvas class="p-5" use:chartJS={data} id="myChart"></canvas>
            </div>
        </div>
</div>