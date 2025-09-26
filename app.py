import streamlit as st  # type: ignore
from graphviz import Digraph, Source  # type: ignore
from PIL import Image  # type: ignore
import pydot  # type: ignore
from index import getDeepDive, isValidURL, mermaidChart, brainMap, eli5, explainBackToMe

firstSubmitFlag = False

st.title("Oboe Extended Features")
with st.form("my_form"):
    myInput = st.text_input('Add your Oboe Course Link Here: ', None)
    submitted = st.form_submit_button("Link")

firstSubmitFlag = True if submitted else firstSubmitFlag

options = ["Mermaid Map", "Mind Map", "ELI5", "Knowledge Check"]
option = st.segmented_control("Choose a feature to try:", options, selection_mode="single")

if myInput and isValidURL(myInput):
    myText = getDeepDive(myInput)
    if not option:
        with st.container(border=True, width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            st.write("Choose a feature above")
    elif option == "Mermaid Map":
        with st.container(border=True, width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            content = mermaidChart(myText)
            content = content.strip().split('\n')[1:-1]
            content = '\n'.join(content)
            graphs = pydot.graph_from_dot_data(content)
            graph = graphs[0]
            svg_data = graph.create_svg().decode("utf-8")
            st.markdown(
                f"""
                <div style="height:700px; width:675px; overflow-y:scroll; overflow-x:scroll; border:1px solid #ddd; text-align:center;">
                    {svg_data}
                """,
                unsafe_allow_html=True,
            )

            with st.expander("🔍 View full graph"):
                st.image(svg_data, width="stretch")
    elif option == "Mind Map":
        with st.container(border=True, width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            content = brainMap(myText)
            content = content.strip().split('\n')[1:-1]
            content = '\n'.join(content)
            graphs = pydot.graph_from_dot_data(content)
            graph = graphs[0]
            svg_data = graph.create_svg().decode("utf-8")
            st.markdown(
                f"""
                <div style="height:700px; width:675px; overflow-y:scroll; overflow-x:scroll; border:1px solid #ddd; text-align:center;">
                    {svg_data}
                """,
                unsafe_allow_html=True,
            )

            with st.expander("🔍 View full graph"):
                st.image(svg_data, width="stretch")
    elif option == "ELI5":
        with st.container(border=True, width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
            st.write(eli5(myText))
    elif option == "Knowledge Check":
        st.write("Lets test your knowlegde. Write down all of the information you remember from learning about this topic, absolutely anything, and we'll help by filling in the gaps.")
        st.session_state.messages = []
        if prompt := st.chat_input("Type Here"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            response = f"Bot: {explainBackToMe(prompt, myText)}"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    with st.container(border=True, width="stretch", height="stretch", horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
        if firstSubmitFlag:
            st.markdown(":red[Please link a valid Oboe Course Link]")