def display_setup(MODEL, X_train, y_train):

    from dtreeviz.trees import dtreeviz
    import numpy as np

    VIZ = dtreeviz(
        MODEL,
        X_train,
        np.ravel(y_train),
        feature_names=X_train.columns,
        target_name='Alvo',
        class_names=['Venda', 'Compra'],
        fancy=True,
        scale=2,
        histtype='barstacked'
    )

    return VIZ


def svg_write(svg, center=True):
    """
    Disable center to left-margin align like other objects.
    """
    import base64
    import streamlit as st

    # Encode as base 64
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")

    # Add some CSS on top
    css_justify = "center" if center else "left"
    css = f'<p style="text-align:center; display: flex; justify-content: {css_justify}">'
    html = f'{css}<img src="data:image/svg+xml;base64,{b64}"/>'

    # Write the HTML
    st.write(html, unsafe_allow_html=True)