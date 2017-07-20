Android ExpandablePanel

While developing an Android app for my final design project, Taedium, I came across what seemed like
a trivial problem. I needed to have a text view (like that in the Android market) that can expand or
collapse whenever a user presses a 'More' or 'Less' button. It turned out that the problem was more
difficult than I thought and I had to make my own custom widget to accomplish the task. I based it
off a partial solution by Peteris Caune over on [Stack Overflow][1].

The basic premise is that we have a custom widget called ExpandablePanel that extends LinearLayout.
This panel in turn expects at least two child Views, a 'content' and a 'handle'.  These can be any
arbitrary Android Views, but typically the content will be a TextView and the handle will be a
Button or ImageButton. When the handle is clicked, the content will expand or collapse to user
specified height. In addition, you can set an onExpand and/or onCollapse listener to handle what
should happen when these actions are fired.

Without further ado, here is the code (comments explaining the basic sections). This code should go
into a file called ExpandablePanel.java:

```java
package com.example.androidapp.widgets;

import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.Transformation;
import android.widget.LinearLayout;

public class ExpandablePanel extends LinearLayout {

    private final int mHandleId;
    private final int mContentId;

    // Contains references to the handle and content views
    private View mHandle;
    private View mContent;

    // Does the panel start expanded?
    private boolean mExpanded = false;
    // The height of the content when collapsed
    private int mCollapsedHeight = 0;
    // The full expanded height of the content (calculated)
    private int mContentHeight = 0;
    // How long the expand animation takes
    private int mAnimationDuration = 0;

    // Listener that gets fired onExpand and onCollapse
    private OnExpandListener mListener;

    public ExpandablePanel(Context context) {
        this(context, null);
    }

    /**
     * The constructor simply validates the arguments being passed in and
     * sets the global variables accordingly. Required attributes are 
     * 'handle' and 'content'
     */
    public ExpandablePanel(Context context, AttributeSet attrs) {
        super(context, attrs);
        mListener = new DefaultOnExpandListener();

        TypedArray a = context.obtainStyledAttributes(
                    attrs, R.styleable.ExpandablePanel, 0, 0);

        // How high the content should be in "collapsed" state
        mCollapsedHeight = (int) a.getDimension(
                    R.styleable.ExpandablePanel_collapsedHeight, 0.0f);

        // How long the animation should take
        mAnimationDuration = a.getInteger(
                    R.styleable.ExpandablePanel_animationDuration, 500);

        int handleId = a.getResourceId(
                    R.styleable.ExpandablePanel_handle, 0);
						
        if (handleId == 0) {
            throw new IllegalArgumentException(
                "The handle attribute is required and must refer "
                    + "to a valid child.");
        }

        int contentId = a.getResourceId(
                        R.styleable.ExpandablePanel_content, 0);
        if (contentId == 0) {
            throw new IllegalArgumentException(
                        "The content attribute is required and must " +
                        "refer to a valid child.");
        }

        mHandleId = handleId;
        mContentId = contentId;

        a.recycle();
    }

    // Some public setters for manipulating the
    // ExpandablePanel programmatically
    public void setOnExpandListener(OnExpandListener listener) {
        mListener = listener; 
    }

    public void setCollapsedHeight(int collapsedHeight) {
        mCollapsedHeight = collapsedHeight;
    }

    public void setAnimationDuration(int animationDuration) {
        mAnimationDuration = animationDuration;
    }

    /**
     * This method gets called when the View is physically
     * visible to the user
     */
    @Override
    protected void onFinishInflate() {
        super.onFinishInflate();

        mHandle = findViewById(mHandleId);
        if (mHandle == null) {
            throw new IllegalArgumentException(
                "The handle attribute is must refer to an"
                    + " existing child.");
        }

        mContent = findViewById(mContentId);
        if (mContent == null) {
            throw new IllegalArgumentException(
                "The content attribute must refer to an"
                    + " existing child.");
        }

	    // This changes the height of the content such that it
        // starts off collapsed
        android.view.ViewGroup.LayoutParams lp = 
                                    mContent.getLayoutParams();
        lp.height = mCollapsedHeight;
        mContent.setLayoutParams(lp);

		// Set the OnClickListener of the handle view
        mHandle.setOnClickListener(new PanelToggler());
    }

    /**
     * This is where the magic happens for measuring the actual
     * (un-expanded) height of the content. If the actual height
     * is less than the collapsedHeight, the handle will be hidden.
     */
    @Override
    protected void onMeasure(int widthMeasureSpec,
                                            int heightMeasureSpec) {
        // First, measure how high content wants to be
        mContent.measure(widthMeasureSpec, MeasureSpec.UNSPECIFIED);
        mContentHeight = mContent.getMeasuredHeight();

        if (mContentHeight &lt; mCollapsedHeight) {
            mHandle.setVisibility(View.GONE);
        } else {
            mHandle.setVisibility(View.VISIBLE);
        }

        // Then let the usual thing happen
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
    }

    /**
     * This is the on click listener for the handle.
     * It basically just creates a new animation instance and fires
     * animation.
     */
    private class PanelToggler implements OnClickListener {
        public void onClick(View v) {
            Animation a;
            if (mExpanded) {
               a = new ExpandAnimation(mContentHeight, mCollapsedHeight);
               mListener.onCollapse(mHandle, mContent);
            } else {
               a = new ExpandAnimation(mCollapsedHeight, mContentHeight);
               mListener.onExpand(mHandle, mContent);
            }
            a.setDuration(mAnimationDuration);
            mContent.startAnimation(a);
            mExpanded = !mExpanded;
        }
    }

    /**
     * This is a private animation class that handles the expand/collapse
     * animations. It uses the animationDuration attribute for the length 
     * of time it takes.
     */
    private class ExpandAnimation extends Animation {
        private final int mStartHeight;
        private final int mDeltaHeight;

        public ExpandAnimation(int startHeight, int endHeight) {
            mStartHeight = startHeight;
            mDeltaHeight = endHeight - startHeight;
        }

        @Override
        protected void applyTransformation(float interpolatedTime, 
                                                 Transformation t) {
            android.view.ViewGroup.LayoutParams lp = 
                                          mContent.getLayoutParams();
            lp.height = (int) (mStartHeight + mDeltaHeight *
                                                   interpolatedTime);
            mContent.setLayoutParams(lp);
        }

        @Override
        public boolean willChangeBounds() {
            return true;
        }
    }

    /**
     * Simple OnExpandListener interface
     */
    public interface OnExpandListener {
        public void onExpand(View handle, View content); 
        public void onCollapse(View handle, View content);
    }

    private class DefaultOnExpandListener implements OnExpandListener {
        public void onCollapse(View handle, View content) {}
        public void onExpand(View handle, View content) {}
    }
}
```

In addition to this file, Android requires you to define any attributes that can be specified from
an xml layout file.  Put this code into your res/values/attrs.xml file:

```xml
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;resources&gt;
    &lt;declare-styleable name="ExpandablePanel"&gt;
        &lt;attr name="handle" format="reference" /&gt;
        &lt;attr name="content" format="reference" /&gt;
        &lt;attr name="collapsedHeight" format="dimension"/&gt;
        &lt;attr name="animationDuration" format="integer"/&gt;
    &lt;/declare-styleable&gt;
&lt;/resources&gt;
```

That's all you need to start using the ExpandablePanel.  Let's see how it works.  The first step is
to define the ExpandablePanel in an xml layout.  Let's pretend we have a file called
res/layouts/panel.xml.  It's contents might look something like this:

```xml
&lt;com.example.androidapp.widgets.ExpandablePanel
    android:id="@+id/foo"
    android:orientation="vertical"
    android:layout_height="wrap_content"
    android:layout_width="fill_parent"
    example:handle="@+id/expand"
    example:content="@+id/value"
    example:collapsedHeight="50dip"
    example:animationDuration="25"&gt;
    &lt;TextView
        android:id="@id/value"
        android:layout_width="fill_parent"
        android:layout_height="wrap_content"/&gt;
    &lt;Button
        android:id="@id/expand"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="More" /&gt;
&lt;/com.example.androidapp.widgets.ExpandablePanel&gt;
```

This works, but when you click the 'More' button the text doesn't get changed to 'Less'. In order to
accomplish this we need to set the listeners:

```java
// Set expandable panel listener
ExpandablePanel panel = (ExpandablePanel)view.findViewById(R.id.foo);
panel.setOnExpandListener(new ExpandablePanel.OnExpandListener() {
    public void onCollapse(View handle, View content) {
        Button btn = (Button)handle;
        btn.setText("More");
    }
    public void onExpand(View handle, View content) {
        Button btn = (Button)handle;
        btn.setText("Less");
    }
});
```

And that's it! If you want to get a nice text fadeout look like the one in the Android market, you
can set/remove a LinearGradient with the content TextView's getPaint().setShader() method. Just add
the shader onCollapse and remove the shader onExpand.

There are still lots of improvements to be made and I'm sure there are a bunch of bugs that I
haven't found, so let me know if something isn't working as it should.

Cheers!

[1]: http://stackoverflow.com/questions/5165682/how-to-implement-expandable-panels-in-android
