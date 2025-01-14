import React, { useState, useContext, useEffect } from "react";
import moment from "moment";
import { useHistory } from "react-router-dom";
import { Dimmer, Loader, Message } from "semantic-ui-react";
import { getSpecificAuthorPost, deletePost } from "../../ApiUtils";
import { Context } from "../../Context";
import PostComponent from "../Post/PostComponent";
import { ROUTE_MY_FEED } from "../../Constants";

const SpecificPostPage = () => {
  const context = useContext(Context);
  let history = useHistory();

  const [loading, updateLoading] = useState(true);
  const [error, updateError] = useState(false);
  const [postInfo, updatePostInfo] = useState([]);

  useEffect(() => {
    callGetPost();
  }, []);

  const callGetPost = async () => {
    const response = await getSpecificAuthorPost(
      context.cookie,
      window.location.pathname
    );

    if (response.status === 200) {
      updatePostInfo([response.data]);
    } else {
      updateError(true);
    }

    updateLoading(false);
  };

  const handleDeletePost = async (id) => {
    let postId = id.split("/");
    postId = postId.slice(-2)[0];

    const response = await deletePost(context.cookie, context.user.id, postId);

    if (response.status !== 204) {
      updateError(true);
    } else {
      history.push(ROUTE_MY_FEED);
    }
  };

  return (
    <div>
      {loading && (
        <Dimmer inverted active>
          <Loader size="medium">Loading Post...</Loader>
        </Dimmer>
      )}
      {error && (
        <Message
          error
          size="large"
          header="Error"
          content="Something happened on our end. Please try again later."
        />
      )}
      {postInfo.map((post, index) => {
        return (
          <div id={index}>
            <PostComponent
              id={post.id}
              title={post.title}
              description={post.description}
              content={post.content}
              contentType={post.contentType}
              author={post.author}
              published={moment(post.published).format(
                "MMMM Do YYYY, h:mm:ss a"
              )}
              visibility={post.visibility}
              handleDeletePost={handleDeletePost}
            />
          </div>
        );
      })}
    </div>
  );
};

export default SpecificPostPage;
