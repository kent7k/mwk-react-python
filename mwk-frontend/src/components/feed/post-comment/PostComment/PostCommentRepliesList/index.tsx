import React from 'react'

// FIXME: cycle/import
// import { PostComment } from ".."
// import { getTimeInfo } from '../../../../../lib/feed'

export function PostCommentRepliesList({ replies }) {
  return replies.map((reply) => (
    <div>{reply}</div>
    // <PostComment
    //     key={reply.id}
    //     id={reply.id}
    //     username={`${reply.author.first_name} ${reply.author.last_name}`}
    //     text={reply.body}
    //     timesince={getTimeInfo(reply.created_at).join(' at ')}
    //     likesCount={reply.like_cnt}
    //     avatarAlt={reply.author.first_name}
    //     avatarSrc={reply.author.avatar}
    //     isLiked={reply.is_user_liked_comment}
    //     replies={[]}
    //     repliesCnt={reply.replies_cnt}
    //  />
  ))
}
