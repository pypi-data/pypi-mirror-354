import gradio as gr
from gradio_consilium_roundtable import consilium_roundtable
import json

def simulate_discussion():
    """Simulate a live AI discussion with custom avatar images"""
    
    # Define avatar images (you can replace these URLs with actual image URLs)
    avatar_images = {
        "QwQ-32B": "https://cdn-avatars.huggingface.co/v1/production/uploads/620760a26e3b7210c2ff1943/-s1gyJfvbE1RgO5iBeNOi.png",
        "DeepSeek-R1": "https://logosandtypes.com/wp-content/uploads/2025/02/deepseek.svg",
        "Mistral Large": "https://logosandtypes.com/wp-content/uploads/2025/02/mistral-ai.svg",
        "Claude": "https://claude.ai/favicon.ico",
        # Web Search Agent will use emoji fallback (no image provided)
    }
    
    # Initial state - everyone ready
    initial_state = {
        "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
        "messages": [],
        "currentSpeaker": None,
        "thinking": [],
        "showBubbles": [],
        "avatarImages": avatar_images
    }

    states = [
        # 1. QwQ-32B starts thinking
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [],
            "currentSpeaker": None,
            "thinking": ["QwQ-32B"],
            "showBubbles": [],
            "avatarImages": avatar_images
        },
        
        # 2. DeepSeek-R1 and Search start thinking - QwQ-32B's bubble should stay visible
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "This is a very long response that should demonstrate the scrolling functionality. I'm going to explain multiple points in detail.\n\n**Key Analysis Points:**\n- First consideration: market dynamics\n- Second factor: technical feasibility\n- Third aspect: resource allocation\n\nWe need to evaluate each of these systematically."}
            ],
            "currentSpeaker": None,
            "thinking": ["DeepSeek-R1", "Web Search Agent"],
            "showBubbles": ["QwQ-32B"],
            "avatarImages": avatar_images
        },
        
        # 3. DeepSeek-R1 responds - both QwQ-32B and DeepSeek-R1 bubbles visible
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "Here's my detailed analysis:\n\n**Key Points:**\n- Market dynamics are shifting rapidly\n- Technical feasibility looks promising\n- Resource allocation needs careful planning\n\n`Implementation roadmap` should include phased rollout."},
                {"speaker": "DeepSeek-R1", "text": "Excellent foundation, QwQ-32B! I'd like to add some **quantitative analysis** to your reasoning:\n\n> Statistical models suggest a 73% success probability\n\nLet me run some deeper calculations..."}
            ],
            "currentSpeaker": "DeepSeek-R1",
            "thinking": [],
            "showBubbles": ["QwQ-32B"],
            "avatarImages": avatar_images
        },
        
        # 4. Multiple models thinking - previous responses stay visible
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "Here's my detailed analysis with key considerations for our strategic approach."},
                {"speaker": "DeepSeek-R1", "text": "Excellent foundation! Statistical models suggest a 73% success probability based on current market conditions."}
            ],
            "currentSpeaker": None,
            "thinking": ["Mistral Large", "Claude"],
            "showBubbles": ["QwQ-32B", "DeepSeek-R1"],
            "avatarImages": avatar_images
        },
        
        # 5. Search agent responds with data - all previous responses visible
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "Here's my detailed analysis with key considerations for our strategic approach."},
                {"speaker": "DeepSeek-R1", "text": "Excellent foundation! Statistical models suggest a 73% success probability based on current market conditions."},
                {"speaker": "Web Search Agent", "text": "📊 **Recent Market Data:**\n\n- Industry growth: +23% YoY\n- Competition analysis: 5 major players\n- Consumer sentiment: 87% positive\n\nSources: MarketWatch, TechCrunch, Industry Reports"}
            ],
            "currentSpeaker": "Web Search Agent",
            "thinking": [],
            "showBubbles": ["QwQ-32B", "DeepSeek-R1"],
            "avatarImages": avatar_images
        },
        
        # 6. Claude joins the discussion
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "Here's my detailed analysis with key considerations for our strategic approach."},
                {"speaker": "DeepSeek-R1", "text": "Statistical models suggest a 73% success probability based on current market conditions."},
                {"speaker": "Web Search Agent", "text": "📊 Industry growth: +23% YoY, Competition: 5 major players, Consumer sentiment: 87% positive"},
                {"speaker": "Claude", "text": "Great insights everyone! Let me synthesize this information:\n\n🎯 **Strategic Recommendation:**\nBased on the quantitative analysis and market data, I suggest a **phased approach** with risk mitigation strategies built in."}
            ],
            "currentSpeaker": "Claude",
            "thinking": [],
            "showBubbles": ["QwQ-32B", "DeepSeek-R1", "Web Search Agent"],
            "avatarImages": avatar_images
        },
        
        # 7. Final consensus with Mistral Large
        {
            "participants": ["QwQ-32B", "DeepSeek-R1", "Mistral Large", "Claude", "Web Search Agent"],
            "messages": [
                {"speaker": "QwQ-32B", "text": "Strategic analysis complete with key considerations outlined."},
                {"speaker": "DeepSeek-R1", "text": "Statistical validation: 73% success probability confirmed."},
                {"speaker": "Web Search Agent", "text": "Market data supports positive outlook: +23% growth, 87% sentiment."},
                {"speaker": "Claude", "text": "Phased approach recommended with integrated risk mitigation."},
                {"speaker": "Mistral Large", "text": "🏆 **CONSENSUS ACHIEVED**\n\nAll analyses converge on a **GO decision** with the following framework:\n\n✅ Phased implementation\n✅ 73% success probability\n✅ Strong market fundamentals\n✅ Risk mitigation protocols"}
            ],
            "currentSpeaker": "Mistral Large",
            "thinking": [],
            "showBubbles": ["QwQ-32B", "DeepSeek-R1", "Web Search Agent", "Claude"],
            "avatarImages": avatar_images
        }
    ]
    
    return initial_state, states

def update_discussion_state(state_index, states):
    """Get the next state in the discussion"""
    if state_index >= len(states):
        state_index = 0
    return states[state_index], state_index + 1

# Initialize the discussion
initial_state, discussion_states = simulate_discussion()

with gr.Blocks() as demo:
    gr.Markdown("# 🎭 Consilium Roundtable Demo")
    gr.Markdown("**Watch the AI discussion unfold!** Click 'Next State' to see different phases of the discussion. 📼 Demo Video: https://youtu.be/oyYlf1BfuU8")
    
    # State management
    state_counter = gr.State(0)
    
    # The roundtable component
    roundtable = consilium_roundtable(
        label="AI Discussion Roundtable",
        show_label=True,
        label_icon="https://huggingface.co/front/assets/huggingface_logo-noborder.svg",
        value=initial_state
    )
    
    with gr.Row():
        next_btn = gr.Button("▶️ Next Discussion State", variant="primary")
        reset_btn = gr.Button("🔄 Reset Discussion", variant="secondary")
    
    # Status display
    with gr.Row():
        status_display = gr.Markdown("**Status:** Discussion ready to begin")
    
    def next_state(current_counter):
        new_state, new_counter = update_discussion_state(current_counter, discussion_states)
        
        # Convert to proper JSON string
        json_state = json.dumps(new_state)
        
        # Create status message
        thinking_list = new_state.get("thinking", [])
        current_speaker = new_state.get("currentSpeaker")
        
        if thinking_list:
            status = f"**Status:** {', '.join(thinking_list)} {'is' if len(thinking_list) == 1 else 'are'} thinking..."
        elif current_speaker:
            status = f"**Status:** {current_speaker} is responding..."
        else:
            status = "**Status:** Discussion in progress..."
            
        return json_state, new_counter, status

    def reset_discussion():
        json_state = json.dumps(initial_state)
        return json_state, 0, "**Status:** Discussion reset - ready to begin"
    
    next_btn.click(
        next_state,
        inputs=[state_counter],
        outputs=[roundtable, state_counter, status_display]
    )
    
    reset_btn.click(
        reset_discussion,
        outputs=[roundtable, state_counter, status_display]
    )

if __name__ == "__main__":
    demo.launch()