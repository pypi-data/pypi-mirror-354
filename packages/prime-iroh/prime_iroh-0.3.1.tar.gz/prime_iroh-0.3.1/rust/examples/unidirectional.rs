/*
 * This example demonstrates simple unidirectional communication between two nodes - one sender and one receiver.
 *
 * Run the receiver:
 *
 * `cargo run --example unidirectional receiver`
 *
 * Run the sender:
 *
 * `cargo run --example unidirectional sender`
 */
use anyhow::Result;
use anyhow::anyhow;
use prime_iroh::node::Node;
use std::env;

fn main() -> Result<()> {
    // Initialize logging
    env_logger::init();

    // Get command line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("Usage: {} [sender|receiver]", args[0]);
        return Err(anyhow!("Usage: {} [sender|receiver]", args[0]));
    }

    let num_streams = 1;
    let num_messages = 5;
    let mode = &args[1];
    let mut node: Node;
    match mode.as_str() {
        "receiver" => {
            // Run the receiver
            println!("Running receiver");
            node = Node::with_seed(num_streams, Some(42))?;

            // Wait for incoming connection
            println!("Waiting for receiver to be ready...");
            while !node.can_recv() {
                std::thread::sleep(std::time::Duration::from_millis(100));
            }
            println!("Ready to receive!");

            // Receive messages
            for i in 0..num_messages {
                let bytes = node.irecv(0)?.wait()?;
                let msg = String::from_utf8_lossy(&bytes);
                println!("Received message {}: {:?}", i + 1, msg);
            }
        }
        "sender" => {
            // Run the sender
            println!("Running sender");
            node = Node::with_seed(num_streams, None)?;

            // Connect to receiver
            println!("Connecting to receiver...");
            // Node address is not available and will trigger discovery error
            let _unavailable_receiver_id =
                String::from("eb1bfc8c80bb48e35e1570c3ded65c32887e0b0c43331c9f7f7a92aabefb2edb");
            let receiver_id =
                String::from("9bdb607f02802cdd126290cfa1e025e4c13bbdbb347a70edeace584159303454");
            node.connect(receiver_id, 10)?;

            // Wait for connection to be established
            println!("Waiting for sender to be ready...");
            while !node.can_send() {
                std::thread::sleep(std::time::Duration::from_millis(100));
            }
            println!("Ready to send!");

            // Send messages
            for i in 0..num_messages {
                let msg = "Hello from sender";
                let bytes = msg.as_bytes().to_vec();
                node.isend(bytes, 0, Some(1000))?.wait()?; // 1s artificial latency
                println!("Sent message {}: {:?}", i + 1, msg);
            }
        }
        _ => {
            return Err(anyhow!("Invalid mode. Use 'sender' or 'receiver'"));
        }
    }

    // Clean up
    println!("Closing node...");
    node.close().unwrap();

    Ok(())
}
