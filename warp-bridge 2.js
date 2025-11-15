import { spawn } from "child_process";



export function runInWarp(command) {

  return new Promise((resolve) => {

    const proc = spawn(command, {

      shell: true,

      stdio: ["ignore", "pipe", "pipe"]

    });



    let output = "";

    let error = "";



    proc.stdout.on("data", (data) => output += data.toString());

    proc.stderr.on("data", (data) => error += data.toString());



    proc.on("close", (code) => {

      resolve({

        success: code === 0,

        code,

        output,

        error

      });

    });

  });

}



if (process.argv[2] === "run") {

  const cmd = process.argv.slice(3).join(" ");

  runInWarp(cmd).then((result) => {

    console.log(JSON.stringify(result, null, 2));

  });

}
